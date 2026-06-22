"""
Qwen3-8B 训练脚本
支持：合并切片 + LoRA 微调
适用：RTX 3060 12GB
"""
import os
import torch
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType

# ============== 配置 ==============
class Config:
    # 模型路径
    SAFETENSORS_DIR = "/media/lz/baba/model/Qwen/Qwen3-8B"  # 5个切片
    MERGED_MODEL_PATH = "/media/lz/baba/model/Qwen3-8B-merged"  # 合并后路径
    OUTPUT_DIR = "/media/lz/baba/smolagents_project/output"
    DATA_PATH = "./data/training_data.json"

    # 训练参数
    NUM_EPOCHS = 3
    LEARNING_RATE = 2e-4
    BATCH_SIZE = 2
    GRADIENT_ACCUM = 8
    MAX_SEQ_LENGTH = 2048

    # LoRA 配置
    LORA_RANK = 64
    LORA_ALPHA = 128
    LORA_DROPOUT = 0.05
    LORA_TARGET_MODULES = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ]

    # 3060 优化
    USE_4BIT = True
    USE_GRADIENT_CHECKPOINT = True


def check_model_files():
    """检查切片文件"""
    print("=" * 50)
    print("检查模型切片文件...")
    print("=" * 50)

    dir_path = Path(Config.SAFETENSORS_DIR)
    safetensors_files = sorted(dir_path.glob("model-*-of-*.safetensors"))

    print(f"找到 {len(safetensors_files)} 个切片文件:")
    for f in safetensors_files:
        size_gb = f.stat().st_size / (1024**3)
        print(f"  {f.name} ({size_gb:.2f} GB)")

    return len(safetensors_files) == 5


def merge_safetensors():
    """合并 safetensors 切片为单个模型"""
    print("\n" + "=" * 50)
    print("合并模型切片...")
    print("=" * 50)

    # 检查是否已合并
    if os.path.exists(Config.MERGED_MODEL_PATH):
        print(f"合并模型已存在: {Config.MERGED_MODEL_PATH}")
        return True

    from safetensors.torch import load_file, save_file

    dir_path = Path(Config.SAFETENSORS_DIR)
    safetensors_files = sorted(dir_path.glob("model-*-of-*.safetensors"))

    merged_state_dict = {}

    for i, file_path in enumerate(safetensors_files):
        print(f"加载 {file_path.name}...")
        state_dict = load_file(str(file_path))

        for key, tensor in state_dict.items():
            # 处理重复key（分布式保存）
            if key in merged_state_dict:
                continue
            merged_state_dict[key] = tensor.cpu()

        del state_dict

    # 保存合并后的模型
    print("保存合并模型...")
    os.makedirs(Config.MERGED_MODEL_PATH, exist_ok=True)

    # 保存为 safetensors 格式
    merged_file = os.path.join(Config.MERGED_MODEL_PATH, "model.safetensors")
    save_file(merged_state_dict, merged_file)

    # 复制配置文件
    import shutil
    for fname in ["config.json", "tokenizer_config.json", "tokenizer.json",
                  "vocab.json", "merges.txt", "generation_config.json"]:
        src = dir_path / fname
        if src.exists():
            shutil.copy(src, Config.MERGED_MODEL_PATH)

    # 处理 model.safetensors.index.json（引用文件）
    index_file = dir_path / "model.safetensors.index.json"
    if index_file.exists():
        with open(index_file) as f:
            index_data = json.load(f)
        # 更新 weight map
        new_index = {
            "metadata": index_data.get("metadata", {}),
            "weight_map": {}
        }
        for key in merged_state_dict.keys():
            new_index["weight_map"][key] = "model.safetensors"
        with open(os.path.join(Config.MERGED_MODEL_PATH, "model.safetensors.index.json"), "w") as f:
            json.dump(new_index, f, indent=2)

    del merged_state_dict
    torch.cuda.empty_cache()

    print(f"合并完成: {Config.MERGED_MODEL_PATH}")
    return True


def prepare_dataset(tokenizer):
    """准备数据集"""
    print("\n" + "=" * 50)
    print("准备数据集...")
    print("=" * 50)

    if not os.path.exists(Config.DATA_PATH):
        print(f"警告: 训练数据不存在: {Config.DATA_PATH}")
        print("创建示例数据...")

        os.makedirs(os.path.dirname(Config.DATA_PATH) or "./data", exist_ok=True)
        sample_data = [
            {
                "instruction": "解释什么是机器学习",
                "input": "",
                "output": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习并改进性能，而无需明确编程。"
            },
            {
                "instruction": "用中文回答",
                "input": "Hello, how are you?",
                "output": "你好，我很好！谢谢关心。"
            }
        ]
        with open(Config.DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        print(f"示例数据已创建: {Config.DATA_PATH}")

    from datasets import load_dataset

    dataset = load_dataset("json", data_files=Config.DATA_PATH, split="train")

    def format_prompt(example):
        return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""

    def tokenize(example):
        prompt = format_prompt(example)
        result = tokenizer(
            prompt,
            truncation=True,
            max_length=Config.MAX_SEQ_LENGTH,
            padding="max_length",
        )
        result["labels"] = result["input_ids"].copy()
        return result

    dataset = dataset.map(tokenize, remove_columns=dataset.column_names)
    print(f"数据集大小: {len(dataset)}")

    return dataset


def load_model_and_tokenizer():
    """加载模型和 tokenizer"""
    print("\n" + "=" * 50)
    print("加载模型...")
    print("=" * 50)

    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        Config.MERGED_MODEL_PATH,
        trust_remote_code=True,
        padding_side="right"
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(
        Config.MERGED_MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
        load_in_4bit=Config.USE_4BIT,
    )

    # 梯度检查点
    if Config.USE_GRADIENT_CHECKPOINT:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    # 打印参数量
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"可训练参数: {trainable_params:,} / {total_params:,} ({100*trainable_params/total_params:.2f}%)")

    return model, tokenizer


def setup_lora(model):
    """设置 LoRA"""
    print("\n" + "=" * 50)
    print("配置 LoRA...")
    print("=" * 50)

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=Config.LORA_RANK,
        lora_alpha=Config.LORA_ALPHA,
        lora_dropout=Config.LORA_DROPOUT,
        target_modules=Config.LORA_TARGET_MODULES,
        bias="none",
    )

    model = get_peft_model(model, lora_config)

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"LoRA 可训练参数: {trainable_params:,} / {total_params:,} ({100*trainable_params/total_params:.2f}%)")

    return model


def train(model, tokenizer, dataset):
    """训练"""
    print("\n" + "=" * 50)
    print("开始训练...")
    print("=" * 50)

    from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq

    training_args = TrainingArguments(
        output_dir=Config.OUTPUT_DIR,
        num_train_epochs=Config.NUM_EPOCHS,
        per_device_train_batch_size=Config.BATCH_SIZE,
        gradient_accumulation_steps=Config.GRADIENT_ACCUM,
        learning_rate=Config.LEARNING_RATE,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        logging_steps=10,
        save_steps=100,
        save_total_limit=3,
        max_grad_norm=0.3,
        fp16=True,
        optim="paged_adamw_8bit",
        gradient_checkpointing=Config.USE_GRADIENT_CHECKPOINT,
        report_to="tensorboard",
        logging_dir=os.path.join(Config.OUTPUT_DIR, "logs"),
        remove_unused_columns=False,
    )

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True,
        max_length=Config.MAX_SEQ_LENGTH,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    trainer.train()

    # 保存
    print(f"\n保存模型到 {Config.OUTPUT_DIR}/final_model")
    trainer.save_model(os.path.join(Config.OUTPUT_DIR, "final_model"))
    tokenizer.save_pretrained(os.path.join(Config.OUTPUT_DIR, "final_model"))

    print("\n训练完成!")


def main():
    print("""
    ╔═══════════════════════════════════════════╗
    ║     Qwen3-8B LoRA 训练脚本                  ║
    ║     适用环境: RTX 3060 12GB                 ║
    ╚═══════════════════════════════════════════╝
    """)

    # 1. 检查切片
    if not check_model_files():
        print("错误: 需要 5 个切片文件")
        return

    # 2. 合并切片
    merge_safetensors()

    # 3. 加载模型
    model, tokenizer = load_model_and_tokenizer()

    # 4. 设置 LoRA
    model = setup_lora(model)

    # 5. 准备数据
    dataset = prepare_dataset(tokenizer)

    # 6. 训练
    train(model, tokenizer, dataset)


if __name__ == "__main__":
    main()
