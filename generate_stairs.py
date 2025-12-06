import random
import json
import zipfile
import os


def generate_stairs(length: int, n: int, min_steps: int = 5) -> list:
    """
    生成一个指定长度的楼梯序列
    生成音游中常见的"楼梯"结构，保证楼梯长度较长，不会频繁调转增减方向
    
    参数:
        length: 列表长度
        n: 元素的最大值（范围是1到n，包括1和n）
        min_steps: 改变方向前的最小步数，用于避免频繁调转方向（默认5）
    
    返回:
        一个满足条件的列表，相邻元素差为1，值在[1, n]范围内
    
    示例:
        >>> generate_stairs(10, 5)
        [3, 4, 5, 4, 3, 2, 1, 2, 3, 4]
    """
    if length <= 0:
        return []
    if n < 1:
        raise ValueError("n必须大于等于1")
    
    result = []
    current = random.randint(1, n)
    direction = random.choice([1, -1])
    steps_in_direction = 0
    
    for i in range(length):
        result.append(current)
        
        # 检查特殊模式：检测最近5个元素
        if len(result) >= 5:
            last_5 = result[-5:]
            # 检测到 21212 模式，下一个强制改为3
            if last_5 == [2, 1, 2, 1, 2]:
                current = 3
                direction = 1 if current < n else -1
                steps_in_direction = 0
                continue
            # 检测到 56565 模式，下一个强制改为4
            elif last_5 == [5, 6, 5, 6, 5]:
                current = 4
                direction = -1 if current > 1 else 1
                steps_in_direction = 0
                continue
        
        # 检查边界
        if current == 1:
            direction = 1
            steps_in_direction = 0
        elif current == n:
            direction = -1
            steps_in_direction = 0
        
        # 如果还没走够最小步数，继续当前方向
        if steps_in_direction < min_steps:
            current += direction
            steps_in_direction += 1
        else:
            # 计算到边界的距离
            dist_to_top = n - current
            dist_to_bottom = current - 1
            
            # 如果接近边界，提前改变方向
            if dist_to_top < min_steps and direction == 1:
                direction = -1
                steps_in_direction = 0
            elif dist_to_bottom < min_steps and direction == -1:
                direction = 1
                steps_in_direction = 0
            else:
                # 随机决定是否改变方向（概率较低，保持长楼梯）
                if random.random() < 0.4:  # 20%概率改变方向
                    direction = -direction
                    steps_in_direction = 0
            
            current += direction
            steps_in_direction += 1
    
    return result


def visualize_stairs(stairs: list, n: int) -> None:
    """
    可视化显示楼梯序列
    每行对应一个时间点，每列对应一个值（从1到n，从左到右）
    在对应位置显示#，空位置显示~
    
    参数:
        stairs: 楼梯序列
        n: 元素的最大值
    """
    if not stairs:
        return
    
    # 每行对应一个时间点
    for pos in stairs:
        line = ""
        # 每列对应一个值（从1到n，从左到右）
        for value in range(1, n + 1):
            if pos == value:
                line += "#"
            else:
                line += "~"
        print(line)


def write_chart_file(stairs: list, output_file: str, sound_file: str = "1749734502.ogg") -> None:
    """
    将楼梯序列写入铺面文件（直接生成完整文件）
    
    参数:
        stairs: 楼梯序列（值在1-6之间）
        output_file: 输出的铺面文件路径
        sound_file: 音频文件名（默认"1761922659.ogg"）
    """
    import time
    
    # 生成note数据
    notes = []
    for i, pos in enumerate(stairs):
        # 计算beat：每小节能容纳4个8分音符
        bar = i // 4  # 小节数
        beat_index = i % 4  # 小节内的位置（0, 1, 2, 3）
        
        # column从0-5（楼梯序列是1-6，需要减1）
        column = pos - 1
        
        note = {
            "beat": [bar, beat_index, 4],
            "column": column
        }
        notes.append(note)
    
    # 在note列表最后添加sound类型的note
    sound_note = {
        "beat": [0, 0, 1],
        "sound": sound_file,
        "vol": 100,
        "offset": 2,
        "type": 1
    }
    notes.append(sound_note)
    
    # 创建完整的铺面数据结构
    data = {
        "meta": {
            "$ver": 0,
            "creator": "",
            "background": "",
            "version": "-New",
            "id": 0,
            "mode": 0,
            "time": int(time.time()),
            "song": {
                "title": "_temp_1761922659",
                "artist": "Unknown",
                "id": 0
            },
            "mode_ext": {
                "column": 6,
                "bar_begin": 0
            }
        },
        "time": [
            {
                "beat": [0, 0, 1],
                "bpm": 130.0
            }
        ],
        "effect": [],
        "note": notes,
        "extra": {
            "test": {
                "divide": 4,
                "speed": 100,
                "save": 0,
                "lock": 0,
                "edit_mode": 0
            }
        }
    }
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"已生成铺面文件: {output_file}")
    print(f"共生成 {len(notes) - 1} 个note（不包括sound note）")
    
    return output_file


if __name__ == "__main__":
    # 示例使用
    '''
    print("示例1: 长度为20，范围1-5")
    stairs1 = generate_stairs(20, 5, min_steps=4)
    print(stairs1)
    print()
    
    print("示例2: 长度为30，范围1-7")
    stairs2 = generate_stairs(30, 7, min_steps=5)
    print(stairs2)
    print()
    '''
    # 生成200行的楼梯序列
    print("生成200行楼梯序列（范围1-6）")
    stairs = generate_stairs(800, 6, min_steps=1)
    print(f"序列长度: {len(stairs)}")
    print()
    
    print("可视化显示（前20行）:")
    visualize_stairs(stairs[:20], 6)
    print()
    
    # 验证相邻元素差为1
    print("验证相邻元素差:")
    error_count = 0
    for i in range(len(stairs) - 1):
        diff = abs(stairs[i+1] - stairs[i])
        if diff != 1:
            print(f"错误: 位置{i}和{i+1}的差为{diff}")
            error_count += 1
    if error_count == 0:
        print("验证完成: 所有相邻元素差都为1")
    print()
    
    # 写入铺面文件
    output_file = "114514.mc"
    mc_file = write_chart_file(stairs, output_file)
    
    # 打包为.mcz文件
    ogg_file = "17491749734502.ogg"
    if not os.path.exists(ogg_file):
        # 如果文件不存在，尝试使用1749734502.ogg
        ogg_file = "1749734502.ogg"
    
    if os.path.exists(ogg_file):
        mcz_file = output_file.replace(".mc", ".mcz")
        with zipfile.ZipFile(mcz_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(mc_file, os.path.basename(mc_file))
            zipf.write(ogg_file, os.path.basename(ogg_file))
        print(f"已生成压缩包: {mcz_file}")
    else:
        print(f"警告: 找不到音频文件 {ogg_file}，无法生成.mcz文件")

