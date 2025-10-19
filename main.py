#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import math
import random
import sys
from datetime import datetime, timedelta
import threading
from typing import Dict, List, Any

class FusionGame:
    def __init__(self):
        # 游戏状态变量
        self.USER = "user"
        self.ADMIN_PASS = "admin123"
        self.COMMAND_COUNT = 0
        self.FUSION_COMMAND_COUNT = 0
        self.HAS_LEFT_PORT = False
        self.IN_PORT = True
        self.PORT_DETACHED = False
        self.FOLI_CONFIGURED = False
        self.AC_ACTIVATED = False
        self.HC_ACTIVATED = False
        self.AGENT_NAME = ""
        
        # 飞船核心状态
        self.SPEED = 0
        self.SPEED_UNIT = "km/h"
        self.THRUSTER_POWER = 0
        self.SPECIFIC_IMPULSE = 0
        self.POSITION = "地球"
        self.EARTH_TIME = datetime.now()
        self.SHIP_TIME = self.EARTH_TIME
        self.SHIP_STATE = "未启动"
        self.MALFUNCTION = "无"
        self.FUSION_STATE = "关闭"
        self.PREPROCESS_EVENT = "无"
        self.SPEED_C = 0.0
        self.TORQUE_RATIO = "1:1"
        self.CONST_PHASE = "false"
        self.FUSION_ENERGY = 0
        self.ENERGY_CONSUMED = 0
        self.TOTAL_ENERGY_CONSUMED = 0
        self.NEG_FIELD_PERCENT = "未启动"
        self.POS_FIELD_PERCENT = "未启动"
        self.BUBBLE_PERCENT = "未启动"
        self.LATITUDE = "地球同步轨道"
        self.DISTANCE_KM = 0.0
        self.LIGHT_YEARS_TRAVELED = 0.0
        self.DISTANCE_AU = 0.0
        self.TEMPERATURE = 0
        self.PRESSURE_RATIO = "1:1"
        
        # 物理常数
        self.SOLAR_SYSTEM_RADIUS_KM = 4.4879e9  # 30 AU in km
        self.OBSERVABLE_UNIVERSE_LY = 46500000000  # 46.5 billion light years
        self.AU_TO_KM = 149597870.7  # 1 AU in km
        self.LY_TO_KM = 9460730472580.8  # 1 light year in km
        
        # 成就系统
        self.ACHIEVEMENTS = []
        
        # 引擎组件状态
        self.FUSION_ENGINE_ON = False
        self.LEIDEN_MODULE = False
        self.ENERGY_STORAGE_ON = False
        self.MAIN_FUSION_ON = False
        self.CLOCK_LOCKED = False
        self.ALCUBIERRE_COMP = False
        self.HAROLD_COMP = False
        self.RICHARD_RING = False
        self.CURVATURE_DRIVE_ACTIVE = False
        self.NEGATIVE_FIELD_ON = False
        self.POSITIVE_FIELD_ON = False
        self.HEIM_BUBBLE_ON = False
        self.DRIVE_BALANCER_ON = False
        
        # 游戏设置
        self.RANDOM_EVENT_CHANCE = 0.01
        self.GAME_DIR = os.path.expanduser("~/.fusion_game")
        self.SAVE_FILE = os.path.join(self.GAME_DIR, "savegame.dat")
        self.LOG_FILE = os.path.join(self.GAME_DIR, "flight_log.txt")
        self.CPSNA_FILE = os.path.join(self.GAME_DIR, "CPSNA.txt")
        
        # 创建游戏目录
        os.makedirs(self.GAME_DIR, exist_ok=True)
        
        # 命令映射
        self.COMMANDS = {
            "pfe": self.start_fusion_engine,
            "sfe": self.stop_fusion_engine,
            "openleiden": self.open_leiden_module,
            "ses": self.start_energy_storage,
            "f": self.start_main_fusion,
            "clock": self.lock_values,
            "unclock": self.unlock_values,
            "ly": self.show_light_years,
            "ccu": self.cooling_curvature,
            "ac": self.start_alcubierre_component,
            "hc": self.start_harold_component,
            "sr": self.start_richard_ring,
            "SR": self.stop_richard_ring,
            "pi": self.energy_pour_into,
            "tr": self.set_torque_ratio,
            "m+": self.start_negative_field,
            "m-": self.start_positive_field,
            "Heim": self.start_heim_bubble,
            "drive": self.start_curvature_drive,
            "sas": self.stop_all_systems,
            "year": self.detect_year,
            "status": self.show_detailed_status,
            "log": self.show_flight_log,
            "help": self.show_help,
            "exit": self.exit_game,
            "quit": self.exit_game,
            "ca": self.change_curvature,
            "pre": self.detach_port,
            "foli": self.configure_foli
        }

    def safe_division(self, a, b):
        """安全除法，避免除零错误"""
        if abs(b) < 1e-10:
            return float('inf') if a >= 0 else float('-inf')
        return a / b

    def log_event(self, event: str):
        """记录事件到日志文件"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {event}\n")

    def typewriter_effect(self, text: str, delay: float = 0.05):
        """打字机效果显示文本"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_art(self):
        """显示艺术字"""
        art = """
███████╗██╗   ██╗███████╗██╗██████╗ ██████╗ ███╗   ██╗
██╔════╝██║   ██║██╔════╝██║██╔══██╗██╔══██╗████╗  ██║
█████╗  ██║   ██║███████╗██║██████╔╝██████╔╝██╔██╗ ██║
██╔══╝  ██║   ██║╚════██║██║██╔══██╗██╔══██╗██║╚██╗██║
██║     ╚██████╔╝███████║██║██║  ██║██████╔╝██║ ╚████║
╚═╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝
        """
        print("\033[1;36m")  # 青色
        print(art)
        print("\033[0m")

    def show_about(self):
        """显示关于信息"""
        about_info = """
\033[1;35m关于 Fusion Game\033[0m
\033[1;32m作者:\033[0m 怡境梦呓
\033[1;32mQQ:\033[0m 2024335187
\033[1;32m邮箱:\033[0m 2024335187@qq.com
\033[1;32mGitHub:\033[0m 未发布
\033[1;32m版本:\033[0m beta 0.5 公开测试版

\033[1;33m阿尔库g-05型光速末日飞船模拟器\033[0m
基于广义相对论与曲率驱动理论的科幻模拟
        """
        print(about_info)

    def admin_login(self):
        """管理员登录剧情"""
        self.clear_screen()
        self.show_art()
        
        print("\033[1;32m", end='')
        self.typewriter_effect("欢迎您使用'阿尔库g-05型'光速末日飞船", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("您一定还记得，当时签下的《反末日法西斯安全合同》", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("您现在乘坐的，是人类第五型最安全的空间曲率驱动飞船", 0.03)
        time.sleep(1)
        
        print("\033[1;31m", end='')
        self.typewriter_effect("请让我再次复述，您的任务是——走到宇宙尽头", 0.04)
        print("\033[1;32m", end='')
        time.sleep(1)
        
        self.typewriter_effect("根据第一型所证实的'爱因斯坦相对论'", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("根据您的参照系，当运行时间够久，您大概率会代替全人类看到宇宙末日", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("您是安全的", 0.05)
        time.sleep(1)
        
        self.typewriter_effect("请为人类社会实现您最后的价值", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("正如合同所说，您的家庭会被社会滋养，被万人罩棚", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("您可以开始了", 0.05)
        time.sleep(1)
        
        self.typewriter_effect("当前状态:位于'末日'型贰号发射井，冷却液已填充完成", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("您将会看到飞船终端", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("如果遗忘了之前培训的启动方式和过程", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("所导致人类社会被毁灭", 0.04)
        time.sleep(1)
        
        self.typewriter_effect("合同内容作废", 0.05)
        time.sleep(1)
        
        self.typewriter_effect("同时，为遵循人性化", 0.03)
        time.sleep(1)
        
        self.typewriter_effect("我们在终端的私有文件夹中存放有txt格式的启动教程", 0.03)
        time.sleep(1)
        
        print("\033[1;32m", end='')
        self.typewriter_effect("请输入 'pre' 开始脱离发射港程序", 0.03)
        print("\033[0m")
        time.sleep(2)

    def add_achievement(self, achievement: str):
        """添加成就"""
        if achievement not in self.ACHIEVEMENTS:
            self.ACHIEVEMENTS.append(achievement)
            print(f"\033[1;33m🎉 获得成就: {achievement}\033[0m")
            self.log_event(f"获得成就: {achievement}")

    def check_random_event(self):
        """检查随机事件"""
        if random.random() < self.RANDOM_EVENT_CHANCE:
            self.MALFUNCTION = "推进零件故障(概率事件)"
            print("\033[1;31m⚠️ 警告: 检测到随机部件故障！\033[0m")
            self.log_event("随机事件: 部件故障")
            
            if self.FUSION_ENGINE_ON:
                self.THRUSTER_POWER = max(0, self.THRUSTER_POWER - 5)
                self.SPEED = max(0, self.SPEED - 50)
            return True
        return False

    def update_position(self):
        """更新位置信息 - 基于真实物理"""
        if self.CURVATURE_DRIVE_ACTIVE:
            # 曲率驱动下的距离计算
            speed_km_per_sec = self.SPEED_C * 299792.458  # 光速 km/s
            distance_increment = speed_km_per_sec * 0.1  # 每0.1秒增加的距离
            self.DISTANCE_KM += distance_increment
        elif self.MAIN_FUSION_ON:
            # 常规推进下的距离计算
            speed_km_per_sec = self.SPEED / 3600  # km/h to km/s
            distance_increment = speed_km_per_sec * 0.1
            self.DISTANCE_KM += distance_increment
        
        # 更新其他距离单位
        self.DISTANCE_AU = self.DISTANCE_KM / self.AU_TO_KM
        self.LIGHT_YEARS_TRAVELED = self.DISTANCE_KM / self.LY_TO_KM
        
        # 更新位置描述
        if self.DISTANCE_KM < 100000:  # 100,000 km
            self.POSITION = "地球轨道"
            self.LATITUDE = "近地轨道"
        elif self.DISTANCE_KM < 384400:  # 月球距离
            self.POSITION = "地月系统"
            self.LATITUDE = "地月转移轨道"
        elif self.DISTANCE_KM < self.SOLAR_SYSTEM_RADIUS_KM:
            self.POSITION = "太阳系内"
            self.LATITUDE = f"距离太阳 {self.DISTANCE_AU:.2f} AU"
        elif self.DISTANCE_KM < 0.1 * self.LY_TO_KM:  # 0.1 光年
            self.POSITION = "近太阳系区域【危险】"
            self.LATITUDE = "本地星际云"
        elif self.DISTANCE_KM < 1 * self.LY_TO_KM:  # 1 光年
            self.POSITION = "外太空地区猎户座左旋臂"
            self.LATITUDE = "本地泡"
        else:
            self.POSITION = "深空"
            self.LATITUDE = f"距离地球 {self.LIGHT_YEARS_TRAVELED:.2f} 光年"

    def update_time(self):
        """更新时间"""
        self.EARTH_TIME = datetime.now()
        if self.CURVATURE_DRIVE_ACTIVE and self.SPEED_C > 0.1:
            # 安全的时间膨胀计算
            try:
                time_dilation = self.safe_division(1, math.sqrt(1 - min(0.999999, self.SPEED_C ** 2)))
                time_shift = self.LIGHT_YEARS_TRAVELED * 0.1 * time_dilation
                self.SHIP_TIME = self.EARTH_TIME + timedelta(seconds=time_shift)
            except (ValueError, ZeroDivisionError):
                self.SHIP_TIME = self.EARTH_TIME
        else:
            self.SHIP_TIME = self.EARTH_TIME

    def format_distance(self, distance_km):
        """格式化距离显示"""
        if distance_km >= 1e9:
            return f"{distance_km:.4e}"
        else:
            return f"{distance_km:,.0f}"

    def show_panel(self):
        """显示数值面板"""
        self.clear_screen()
        print("=" * 80)
        print("                阿尔库g-05型光速末日飞船 - 控制系统")
        print("=" * 80)
        
        # 速度显示
        speed_display = f"{self.SPEED_C:.3f}" if self.SPEED_UNIT == "c" else f"{self.SPEED}"
        if self.SPEED == 0 and self.SPEED_C == 0:
            speed_display = "\033[31m尚无\033[0m"
        
        # 功率显示
        power_display = f"{self.THRUSTER_POWER}%"
        if self.THRUSTER_POWER == 0:
            power_display = "\033[31m尚无\033[0m"
        
        # 比冲显示
        impulse_display = f"{self.SPECIFIC_IMPULSE}"
        if self.SPECIFIC_IMPULSE == 0:
            impulse_display = "\033[31m尚无\033[0m"
        
        # 距离显示
        distance_color = "\033[32m" if self.DISTANCE_KM >= self.SOLAR_SYSTEM_RADIUS_KM else "\033[31m"
        distance_display = f"{distance_color}{self.format_distance(self.DISTANCE_KM)} km\033[0m"
        
        print(f"速度({self.SPEED_UNIT}): {speed_display:<15} 推进器功率: {power_display:<10} 比冲: {impulse_display:<10}")
        print(f"位置: {self.POSITION:<20} 时间: {self.SHIP_TIME.strftime('%Y-%m-%d %H:%M:%S'):<30}")
        print(f"航行距离: {distance_display:<20} AU: {self.DISTANCE_AU:.6f}")
        
        # 故障显示
        malfunction_display = self.MALFUNCTION
        if self.MALFUNCTION != "无":
            malfunction_display = f"\033[31m{self.MALFUNCTION}\033[0m"
        
        print(f"当前状态: {self.SHIP_STATE:<15} 故障: {malfunction_display:<20}")
        print(f"聚变发动机状态: {self.FUSION_STATE:<10} 预处理事件: {self.PREPROCESS_EVENT:<15}")
        print(f"当前速度(c): {self.SPEED_C:<10.3f} 扭矩比: {self.TORQUE_RATIO:<10} 恒定阶段: {self.CONST_PHASE:<10}")
        
        # 能量显示（科学计数法防止溢出）
        fusion_energy_str = f"{self.FUSION_ENERGY:.2e}" if self.FUSION_ENERGY > 1e12 else f"{self.FUSION_ENERGY}"
        energy_consumed_str = f"{self.ENERGY_CONSUMED:.2e}" if self.ENERGY_CONSUMED > 1e12 else f"{self.ENERGY_CONSUMED}"
        total_energy_str = f"{self.TOTAL_ENERGY_CONSUMED:.2e}" if self.TOTAL_ENERGY_CONSUMED > 1e12 else f"{self.TOTAL_ENERGY_CONSUMED}"
        
        print(f"聚变发动机产生能量: {fusion_energy_str:<15}J 当前操作预消耗能量: {energy_consumed_str:<15}J")
        print(f"已消耗的能量: {total_energy_str:<15}J 纬度: {self.LATITUDE:<20}")
        
        # 场生成显示
        neg_field_display = self.NEG_FIELD_PERCENT
        if self.NEG_FIELD_PERCENT == "未启动":
            neg_field_display = f"\033[31m{self.NEG_FIELD_PERCENT}\033[0m"
        else:
            neg_field_display = f"{self.NEG_FIELD_PERCENT}%"
            
        pos_field_display = self.POS_FIELD_PERCENT
        if self.POS_FIELD_PERCENT == "未启动":
            pos_field_display = f"\033[31m{self.POS_FIELD_PERCENT}\033[0m"
        else:
            pos_field_display = f"{self.POS_FIELD_PERCENT}%"
            
        bubble_display = self.BUBBLE_PERCENT
        if self.BUBBLE_PERCENT == "未启动":
            bubble_display = f"\033[31m{self.BUBBLE_PERCENT}\033[0m"
        else:
            bubble_display = f"{self.BUBBLE_PERCENT}%"
        
        print(f"负能场: {neg_field_display:<15} 正能场: {pos_field_display:<15} 曲率泡: {bubble_display:<15}")
        
        # 聚变参数显示
        if self.TEMPERATURE > 0:
            print(f"聚变温度: {self.TEMPERATURE}℃ 压力比: {self.PRESSURE_RATIO}")
        
        # 成就显示
        if self.ACHIEVEMENTS:
            print("-" * 80)
            print(f"成就: {' '.join(self.ACHIEVEMENTS)}")
        
        print("=" * 80)
        print()

    def parse_command(self, input_str: str):
        """解析命令"""
        parts = input_str.strip().split()
        if not parts:
            return None, [], ""
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        remaining = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        return cmd, args, remaining

    def process_command(self, cmd: str, args: List[str]):
        """处理命令"""
        self.COMMAND_COUNT += 1
        
        # 成就检查
        if self.COMMAND_COUNT == 1:
            self.add_achievement("山姆大叔需要你！")
        elif self.COMMAND_COUNT == 10:
            self.add_achievement("fu*k！")
        
        # 检查是否在发射港中
        if self.IN_PORT and not self.PORT_DETACHED and cmd not in ["pre", "help", "exit", "quit"]:
            return "❌ 错误: 请先脱离发射港 (输入 'pre')"
        
        if cmd in self.COMMANDS:
            return self.COMMANDS[cmd](args)
        else:
            return f"未知命令: {cmd}\n输入 'help' 查看可用命令"

    # 新增命令实现
    def change_curvature(self, args):
        """改变曲率驱动光速"""
        if len(args) < 1:
            return "错误: 需要参数 <光速倍数>"
        
        try:
            new_speed_c = float(args[0])
            if new_speed_c < 0:
                return "错误: 光速倍数必须为正数"
            
            self.SPEED_C = new_speed_c
            self.log_event(f"改变曲率驱动光速: {new_speed_c}c")
            return f"✅ 曲率驱动光速已设置为: {new_speed_c}c"
        except ValueError:
            return "错误: 参数必须为数字"

    def detach_port(self, args):
        """脱离发射港"""
        if self.PORT_DETACHED:
            return "❌ 发射港已脱离，无法重复执行"
        
        if len(args) == 0:
            # 第一阶段脱离
            print("\033[33m正在启动聚变发动机指定脱港GF-71协议中。\033[0m")
            time.sleep(1)
            print("\033[32m正在脱离卸钩，发射港脱离中……\033[0m")
            time.sleep(3)
            print("发射港状态:【已脱离】")
            time.sleep(10)
            print("您现在已脱离钱学森伍形发射港，人类社会将对您舍生的精神抱以诚挚的感谢和敬意！")
            self.PORT_DETACHED = True
            self.IN_PORT = False
            self.log_event("脱离发射港完成")
            return ""
        
        elif len(args) == 2:
            # 第二阶段发动机授权
            print("\033[32m已授权发动机指令。\033[0m")
            time.sleep(1)
            print("正在脱冷预热中……")
            time.sleep(3)
            print("当前发动机为:【氢氦聚变发动机】，已设置好功率和比冲，请输入 'foli [温度(℃)] [压力比]'，以启动聚变发动机。")
            self.THRUSTER_POWER = int(args[0])
            self.SPECIFIC_IMPULSE = int(args[1])
            return ""
        
        return "错误: 参数数量不正确"

    def configure_foli(self, args):
        """配置氢氦聚变发动机"""
        if len(args) < 2:
            return "错误: 需要参数 <温度> <压力比>"
        
        try:
            temperature = int(args[0])
            pressure_ratio = args[1]
            
            if temperature < 1000:
                return "错误: 温度过低，至少需要1000℃"
            
            if ":" not in pressure_ratio:
                return "错误: 压力比格式应为 原始量:现在量 (如 1:2)"
            
            self.TEMPERATURE = temperature
            self.PRESSURE_RATIO = pressure_ratio
            self.FOLI_CONFIGURED = True
            self.log_event(f"配置聚变发动机 - 温度: {temperature}℃, 压力比: {pressure_ratio}")
            
            print("已设置完成，输入 'drive a'，来启动发动机。")
            return ""
        except ValueError:
            return "错误: 温度必须为整数"

    def start_fusion_drive_a(self):
        """启动聚变发动机 (drive a)"""
        if not self.FOLI_CONFIGURED:
            return "❌ 错误: 请先配置聚变发动机 (foli命令)"
        
        print("\033[33m(2秒)聚变发动机已启动\033[0m")
        time.sleep(2)
        print("(3秒)您已踏上宇宙的旅途，请记住，地球，永远是你的家。")
        time.sleep(3)
        print("(4秒)当前已航行出黄色违禁区，请启动主聚变引擎30。")
        
        self.FUSION_ENGINE_ON = True
        self.SHIP_STATE = "氢氦聚变推进"
        self.SPEED = 10000  # 初始速度
        self.log_event("启动氢氦聚变发动机")
        
        return ""

    # 修改现有的命令实现
    def start_fusion_engine(self, args):
        if self.IN_PORT and not self.PORT_DETACHED:
            return "❌ 错误: 请先脱离发射港"
        
        if len(args) < 2:
            return "错误: 需要参数 <功率> 和 <比冲>"
        
        try:
            power = int(args[0])
            impulse = int(args[1])
        except ValueError:
            return "错误: 参数必须为整数"
        
        if power < 1 or power > 100:
            return "错误: 功率必须在 1-100 之间"
        
        if impulse < 1000 or impulse > 50000:
            return "错误: 比冲必须在 1000-50000 之间"
        
        self.THRUSTER_POWER = power
        self.SPECIFIC_IMPULSE = impulse
        self.SPEED = power * 1000  # 增加基础速度
        self.SHIP_STATE = "启动聚变脉冲推进器中"
        self.FUSION_STATE = "运行中"
        self.FUSION_ENGINE_ON = True
        self.ENERGY_CONSUMED = power * impulse // 10
        self.TOTAL_ENERGY_CONSUMED += self.ENERGY_CONSUMED
        
        self.FUSION_COMMAND_COUNT += 1
        if self.FUSION_COMMAND_COUNT == 1:
            self.add_achievement("路易十六是交叉感染死的")
        
        self.log_event(f"启动聚变脉冲推进器 - 功率: {power}%, 比冲: {impulse}")
        result = f"✅ 聚变脉冲推进器启动 - 功率: {power}% 比冲: {impulse}"
        
        # 检查随机事件
        if self.check_random_event():
            result += "\n⚠️ 随机事件: 检测到部件故障！"
        
        return result

    def start_main_fusion(self, args):
        if len(args) < 1:
            return "错误: 需要参数 <功率>"
        
        try:
            power = int(args[0])
        except ValueError:
            return "错误: 参数必须为整数"
        
        if not self.ENERGY_STORAGE_ON:
            self.MALFUNCTION = "能量过载风险"
            self.log_event("错误尝试: 未启动能量栈堆即启动主聚变堆")
            return "❌ 错误: 请先启动能量栈堆 (ses)"
        
        if power > 150:
            self.MALFUNCTION = "发动机热锁死"
            self.log_event(f"发动机热锁死 - 功率过高: {power}%")
            self.add_achievement("发动机！")
            return "❌ 错误: 功率过高，发动机热锁死"
        
        self.MAIN_FUSION_ON = True
        self.THRUSTER_POWER = power
        self.SPEED = power * 10000  # 大幅增加速度
        self.SHIP_STATE = "常规推进"
        self.FUSION_ENERGY = power * 1000000000
        self.ENERGY_CONSUMED = power * 1000000
        self.TOTAL_ENERGY_CONSUMED += self.ENERGY_CONSUMED
        
        self.log_event(f"启动主聚变堆 - 功率: {power}%")
        
        # 显示航行信息
        result = f"✅ 已启动主聚变发动机，当前功率: {power}%，速度为: {self.SPEED} km/h\n"
        result += f"   加速比: 1:{power//10}\n"
        result += "   航行开始！\n"
        
        # 模拟航行过程
        print(result)
        for i in range(5):
            time.sleep(1)
            self.update_position()
            progress = min(100, (self.DISTANCE_KM / self.SOLAR_SYSTEM_RADIUS_KM) * 100)
            distance_color = "\033[32m" if self.DISTANCE_KM >= self.SOLAR_SYSTEM_RADIUS_KM else "\033[31m"
            print(f"   ({i+1}秒)当前航行距离: {distance_color}{self.format_distance(self.DISTANCE_KM)} km\033[0m, "
                  f"AU: {self.DISTANCE_AU:.6f}, "
                  f"已完成: {progress:.2f}%")
        
        if self.DISTANCE_KM >= self.SOLAR_SYSTEM_RADIUS_KM:
            self.add_achievement("太阳系穿越者")
            return "\n🎉 已成功穿越太阳系！可以开始曲率驱动准备。"
        else:
            return f"\n当前进度: {progress:.2f}%，请继续加速或等待。"

    def cooling_curvature(self, args):
        if not self.MAIN_FUSION_ON:
            return "❌ 错误: 请先启动主聚变堆"
        
        print("\033[33m欢迎使用CPSNA研制的预冷却系统，您的聚变发动机正在冷却关停中……\033[0m")
        time.sleep(1)
        print("已达到SPA-02停机标准，授权CCA的曲率驱动预启动程序，感谢您的使用和信任！")
        time.sleep(4)
        
        agent_name = input("请输入您的名称或有象征性的代理名: ")
        self.AGENT_NAME = agent_name
        
        # 创建感谢信
        thank_you_note = f"""
致 {agent_name}:

感谢您使用CPSNA预冷却系统。
您的勇气和奉献精神将被人类文明永远铭记。
在您踏上这段前往宇宙尽头的旅程时，请记住：
地球永远是您的家。

此致
敬礼

CPSNA 全体成员
{datetime.now().strftime('%Y年%m月%d日')}
        """
        
        with open(self.CPSNA_FILE, 'w', encoding='utf-8') as f:
            f.write(thank_you_note)
        
        self.SHIP_STATE = "预曲率驱动"
        self.PREPROCESS_EVENT = "冷却程序中"
        self.log_event("启动曲率驱动冷却系统")
        self.add_achievement("我喜欢这来自暴风雨前的沉浸")
        return "✅ 曲率驱动冷却系统启动 - 准备超光速航行\n   感谢信已保存至 CPSNA.txt"

    def start_alcubierre_component(self, args):
        print("\033[35mCiallo～(∠・ω< )⌒☆\033[0m")
        time.sleep(1)
        print("欢迎使用由一堆二次元研究的ac组件，您们是人类的希望！")
        time.sleep(2)
        print("正在启动修复LLO漏洞程序(检查权限，如:检测到您无权读取$[权限]，修复中)")
        time.sleep(2)
        print("正在启动小鸟葬六花v2.3程序……")
        time.sleep(1)
        
        repair_percent = random.randint(25, 30)
        print(f"此次修复漏洞区{repair_percent}％，残余未知漏洞:0％。地球永远是您的家！")
        
        self.ALCUBIERRE_COMP = True
        self.AC_ACTIVATED = True
        self.log_event("启动Alcubierre稳定性组件")
        
        # 检查是否自动启动Richard环
        if self.AC_ACTIVATED and self.HC_ACTIVATED and not self.RICHARD_RING:
            response = input("正在自启动Richard奇异物质环自启动程序，是否允许程序自启动?(y/n): ")
            if response.lower() == 'y':
                self.RICHARD_RING = True
                self.log_event("Richard奇异物质环自启动")
                time.sleep(1)
                print("IAF和全体人类感谢您为人类做出的贡献，为您致敬。")
                time.sleep(4)
                return "✅ Richard奇异物质环已被打开，感谢您的付出！"
            else:
                return "请自启动程序，IFA留。"
        
        return "✅ Alcubierre稳定性组件已启动"

    def start_harold_component(self, args):
        print("正在启动Harold能量计算")
        time.sleep(2)
        print("启动成功。")
        self.HAROLD_COMP = True
        self.HC_ACTIVATED = True
        self.log_event("启动Harold能量计算组件")
        
        # 检查是否自动启动Richard环
        if self.AC_ACTIVATED and self.HC_ACTIVATED and not self.RICHARD_RING:
            response = input("正在自启动Richard奇异物质环自启动程序，是否允许程序自启动?(y/n): ")
            if response.lower() == 'y':
                self.RICHARD_RING = True
                self.log_event("Richard奇异物质环自启动")
                time.sleep(1)
                print("IAF和全体人类感谢您为人类做出的贡献，为您致敬。")
                time.sleep(4)
                return "✅ Richard奇异物质环已被打开，感谢您的付出！"
            else:
                return "请自启动程序，IFA留。"
        
        return "✅ Harold组件已启动"

    def start_curvature_drive(self, args):
        # 检查是否是聚变发动机启动
        if args and args[0] == "a":
            return self.start_fusion_drive_a()
        
        # 曲率驱动启动
        if self.POSITION in ["地球轨道", "地月系统", "太阳系内"]:
            self.MALFUNCTION = "违法启动曲率驱动"
            self.log_event(f"严重违规: 在 {self.POSITION} 区域尝试启动曲率驱动")
            return "❌ 严重违规: 在禁止区域启动曲率驱动！"
        
        if not self.HEIM_BUBBLE_ON:
            return "❌ 错误: 曲率泡未就绪，请先启动Heim闭合器"
        
        # 安全检查
        print("正在检查中...")
        time.sleep(2)
        
        self.clear_screen()
        print("当前扭矩比:", self.TORQUE_RATIO)
        print("当前前方空间状态: 膨胀")
        print("当前后方空间状态: 收缩")
        print()
        
        # 计算启动时间
        launch_time = random.randint(30, 60)
        print(f"您将于 {launch_time} 秒后进入光速，全体人类再次向您致敬，")
        print("您的名字将会被命名成为任何恒星中的一颗恒星，您会被世人所铭记，")
        print("希望您回来时，地球尚还存在，她任然是你的家！")
        
        # 模拟倒计时
        for i in range(launch_time, 0, -1):
            print(f"\r进入光速倒计时: {i} 秒", end='', flush=True)
            time.sleep(1)
        
        print("\n🚀 曲率驱动启动！")
        
        self.CURVATURE_DRIVE_ACTIVE = True
        self.DRIVE_BALANCER_ON = True
        self.SPEED_C = 1.0
        self.SPEED_UNIT = "c"
        self.SHIP_STATE = "曲率驱动中"
        self.TORQUE_RATIO = "1:3"
        self.CONST_PHASE = "true"
        self.ENERGY_CONSUMED = 1e18
        self.TOTAL_ENERGY_CONSUMED += self.ENERGY_CONSUMED
        
        self.log_event("启动曲率场平衡器 - 进入超光速航行")
        self.add_achievement("这是一个信封")
        
        if self.LIGHT_YEARS_TRAVELED > 100:
            self.add_achievement("前进，不择手段的前进！")
        
        return "✅ 曲率场平衡器启动 - 进入超光速航行！"

    def detect_year(self, args):
        earth_year = 2024 + self.LIGHT_YEARS_TRAVELED
        time_dilation = 1.0
        
        if self.SPEED_C < 1:
            time_dilation = self.safe_division(1, math.sqrt(1 - min(0.999999, self.SPEED_C ** 2)))
        
        result = f"正在计算当前地球元年……\n"
        print(result)
        time.sleep(9)
        
        year_result = f"当前地球元年: {earth_year:.2f}"
        print(year_result)
        
        if earth_year > 2025:
            self.show_ending()
        
        return ""

    def show_ending(self):
        """显示结局"""
        self.clear_screen()
        ending_text = """
感谢您的游玩

开发者:怡境梦呓
相关文献:Near-100% spontaneous rolling up of polar van der Waals materials
无任何不良引导
如果出现bug，请联系作者
再次感谢您的游玩！

这只是测试版！不代表最终品质。
        """
        
        for line in ending_text.split('\n'):
            print(line)
            time.sleep(1)
        
        input("\n按回车键退出...")
        self.exit_game([])

    # 其他命令保持不变（但已修复除零错误）
    def stop_fusion_engine(self, args):
        self.THRUSTER_POWER = 0
        self.SPECIFIC_IMPULSE = 0
        self.SPEED = 0
        self.SHIP_STATE = "停滞"
        self.FUSION_STATE = "关闭"
        self.FUSION_ENGINE_ON = False
        self.MAIN_FUSION_ON = False
        self.ENERGY_CONSUMED = 0
        self.log_event("关闭聚变脉冲推进器")
        return "✅ 聚变脉冲推进器已关闭"

    def open_leiden_module(self, args):
        self.LEIDEN_MODULE = True
        self.log_event("启动莱顿稳定性模块")
        return "✅ 莱顿模块已启动 - 等离子体稳定性增强"

    def start_energy_storage(self, args):
        self.ENERGY_STORAGE_ON = True
        self.log_event("启动能量栈堆系统")
        return "✅ 能量栈堆已启动 - 能量缓冲就绪"

    def lock_values(self, args):
        self.CLOCK_LOCKED = True
        self.log_event("锁定系统数值")
        return "✅ 数值已锁定 - 系统参数固定"

    def unlock_values(self, args):
        self.CLOCK_LOCKED = False
        self.log_event("解除数值锁定")
        return "✅ 数值锁定已解除 - 可调整参数"

    def show_light_years(self, args):
        return f"已行驶距离: {self.LIGHT_YEARS_TRAVELED:.6f} 光年\n相当于 {self.LIGHT_YEARS_TRAVELED * self.LY_TO_KM:.2f} 公里"

    def start_richard_ring(self, args):
        if not self.HAROLD_COMP:
            return "❌ 错误: 请先启动Harold组件 (hc)"
        
        self.RICHARD_RING = True
        self.log_event("启动Richard奇异物质环")
        return "✅ Richard奇异物质环已启动 - 负能量场生成器预热"

    def stop_richard_ring(self, args):
        self.RICHARD_RING = False
        self.NEGATIVE_FIELD_ON = False
        self.NEG_FIELD_PERCENT = "未启动"
        self.log_event("关闭Richard奇异物质环")
        return "✅ Richard奇异物质环已关闭"

    def energy_pour_into(self, args):
        if len(args) < 1:
            return "错误: 需要参数 <能量灌注率>"
        
        try:
            percent = int(args[0])
        except ValueError:
            return "错误: 参数必须为整数"
        
        if percent < 0 or percent > 100:
            return "错误: 灌注率必须在 0-100 之间"
        
        if not self.RICHARD_RING:
            return "❌ 错误: 请先启动Richard奇异物质环 (sr)"
        
        self.ENERGY_CONSUMED = percent * 10000000000000
        self.TOTAL_ENERGY_CONSUMED += self.ENERGY_CONSUMED
        self.log_event(f"能量灌注: {percent}%")
        
        print("(3秒后)已灌注能量:", percent, "%")
        return ""

    def set_torque_ratio(self, args):
        if len(args) < 1:
            return "错误: 需要参数 <扭矩比>"
        
        ratio = args[0]
        if not ":" in ratio:
            return "错误: 扭矩比格式应为 前:后 (如 1:3)"
        
        self.TORQUE_RATIO = ratio
        self.log_event(f"设置扭矩比: {ratio}")
        
        print("(3秒后)已设置扭矩比", ratio)
        return ""

    def start_negative_field(self, args):
        if len(args) < 1 or args[0] != "ture":
            return "❌ 参数错误: 必须使用 'ture' 确认启动"
        
        if self.ENERGY_CONSUMED < 100000000000000:
            return "❌ 错误: 能量灌注不足，请先进行能量灌注 (pi)"
        
        self.NEGATIVE_FIELD_ON = True
        self.NEG_FIELD_PERCENT = 25
        self.log_event("启动负能量场 - 灌注率: 25%")
        
        print("VVVV型负能场启动，填充值: 25")
        return ""

    def start_positive_field(self, args):
        if len(args) < 1 or args[0] != "ture":
            return "❌ 参数错误: 必须使用 'ture' 确认启动"
        
        self.POSITIVE_FIELD_ON = True
        self.POS_FIELD_PERCENT = 100
        self.log_event("启动正能量场 - 灌注率: 100%")
        
        print("IIIII级可型正能场启动，填充值: 100")
        return ""

    def start_heim_bubble(self, args):
        if not self.NEGATIVE_FIELD_ON or not self.POSITIVE_FIELD_ON:
            return "❌ 错误: 请先启动正负能量场"
        
        print("(1秒)正在闭合曲率泡中……")
        time.sleep(4)
        print("(5秒后)已隔绝舱内时空，已成功形成平坦时空舱")
        
        self.HEIM_BUBBLE_ON = True
        self.BUBBLE_PERCENT = 100
        self.log_event("启动曲率泡闭合器")
        return ""

    def stop_all_systems(self, args):
        print("关闭一级系统...")
        time.sleep(1)
        print("关闭二级系统...")
        time.sleep(1)
        print("关闭三级系统...")
        time.sleep(1)
        
        self.CURVATURE_DRIVE_ACTIVE = False
        self.DRIVE_BALANCER_ON = False
        self.HEIM_BUBBLE_ON = False
        self.NEGATIVE_FIELD_ON = False
        self.POSITIVE_FIELD_ON = False
        self.SPEED_C = 0.0
        self.SPEED_UNIT = "km/h"
        self.SPEED = 1000
        self.SHIP_STATE = "测定时间"
        self.NEG_FIELD_PERCENT = "未启动"
        self.POS_FIELD_PERCENT = "未启动"
        self.BUBBLE_PERCENT = "未启动"
        self.log_event("关闭所有曲率系统")
        return "✅ 所有曲率系统关闭，切换至常规推进"

    def show_detailed_status(self, args):
        status = ["=== 详细系统状态 ==="]
        status.append(f"聚变引擎: {self.FUSION_STATE}")
        status.append(f"能量存储: {'在线' if self.ENERGY_STORAGE_ON else '离线'}")
        status.append(f"莱顿模块: {'激活' if self.LEIDEN_MODULE else '未激活'}")
        status.append(f"曲率系统: {'超光速航行' if self.CURVATURE_DRIVE_ACTIVE else '常规航行'}")
        status.append(f"Alcubierre组件: {'就绪' if self.ALCUBIERRE_COMP else '未就绪'}")
        status.append(f"Harold组件: {'计算中' if self.HAROLD_COMP else '待机'}")
        status.append(f"Richard环: {'运行' if self.RICHARD_RING else '关闭'}")
        
        total_energy_str = f"{self.TOTAL_ENERGY_CONSUMED:.2e}" if self.TOTAL_ENERGY_CONSUMED > 1e12 else f"{self.TOTAL_ENERGY_CONSUMED}"
        status.append(f"总能量消耗: {total_energy_str} 焦耳")
        status.append(f"相当于 {self.TOTAL_ENERGY_CONSUMED / 4184000000000000000:.10f} 百万吨TNT")
        return "\n".join(status)

    def show_flight_log(self, args):
        try:
            with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-10:]
            return "=== 飞行日志 (最近10条) ===\n" + "".join(logs)
        except FileNotFoundError:
            return "日志文件不存在"

    def show_help(self, args):
        help_text = """
可用命令:

基础推进系统:
pfe [功率] [比冲]  - 启动聚变脉冲推进器
sfe               - 关闭聚变引擎
openleiden        - 启动莱顿稳定性模块
ses               - 启动能量存储系统
f [功率]          - 启动主聚变堆

曲率驱动系统:
ccu               - 冷却系统预启动
ac                - 启动Alcubierre稳定性组件
hc                - 启动Harold能量计算组件
sr                - 启动Richard奇异物质环
SR                - 关闭Richard环
pi [百分比]       - 能量灌注
tr [前:后]        - 设置扭矩比
m+ [ture]         - 启动负能量场
m- [ture]         - 启动正能量场
Heim              - 曲率泡闭合器
drive             - 曲率场平衡器
drive a           - 启动聚变发动机
sas               - 关闭所有曲率系统

辅助系统:
clock             - 锁定当前数值
unclock           - 解除数值锁定
ly                - 查询光年距离
year              - 探测当前地球年
status            - 详细系统状态
log               - 查看飞行日志
help              - 显示命令帮助
exit              - 退出系统

新增命令:
ca [光速倍数]     - 改变曲率驱动光速
pre               - 脱离发射港
pre [功率] [比冲] - 发动机授权
foli [温度] [压力比] - 配置聚变发动机

注意: 所有命令不用加<>，参数用空格分隔
示例: pfe 10 10000
        """
        return help_text

    def exit_game(self, args):
        self.log_event("用户退出系统")
        print("保存游戏并退出...")
        sys.exit(0)

    def run(self):
        """运行游戏"""
        # 显示初始剧情
        self.admin_login()
        
        # 添加第一个成就
        self.add_achievement("山姆大叔需要你！")
        self.log_event("系统启动 - 用户登录完成")
        
        # 游戏主循环
        while True:
            try:
                self.update_time()
                self.update_position()
                self.show_panel()
                
                user_input = input(f"[{self.USER}@curvature-drive]# ").strip()
                
                if user_input:
                    cmd, args, _ = self.parse_command(user_input)
                    if cmd:
                        result = self.process_command(cmd, args)
                        if result:
                            print(f"\n{result}\n")
                    
                    print("按回车继续...")
                    input()
                
            except KeyboardInterrupt:
                print("\n\n检测到中断信号，退出游戏...")
                self.exit_game([])
            except Exception as e:
                print(f"\n错误: {e}")
                print("按回车继续...")
                input()

if __name__ == "__main__":
    game = FusionGame()
    game.run()