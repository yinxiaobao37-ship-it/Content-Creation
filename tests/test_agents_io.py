import unittest

class MockAgentEcosystem:
    """
    模拟多 Agent 生态系统的工作流
    由于真实的 Agent 需要调用大模型 API，这里我们使用 Mock 的方式，
    根据系统提示词(SKILL.md)的设定，模拟 Router 的调度逻辑和各子 Agent 的标准输出结构。
    """
    def execute(self, user_input):
        # 1. Router 意图解析与分发逻辑
        if "排版" in user_input and "草稿" in user_input and "及格" in user_input:
            # 【复合意图场景】：打分 + 排版
            eval_res = self.call_evaluator(user_input)
            adapt_res = self.call_channel_adapter(user_input)
            return f"🤖 [Router调度执行]\n{eval_res}\n---\n{adapt_res}"
            
        elif "排版" in user_input or "小红书" in user_input or "公众号" in user_input:
            return self.call_channel_adapter(user_input)
            
        elif "打分" in user_input or "评估" in user_input or "草稿" in user_input:
            return self.call_evaluator(user_input)
            
        elif "数据" in user_input or "阅读量" in user_input or "完播率" in user_input:
            return self.call_data_diagnoser(user_input)
            
        else:
            # 兜底路由到内容创作大师
            return self.call_crafting(user_input)

    # 2. 各子 Agent 的标准输出结构模拟
    def call_crafting(self, user_input):
        return (
            "【内容创作大师 (Crafting Master)】响应：\n"
            "好的！让我们进入「5步创作引导法」。\n"
            "第一步：选题阶段。请问你最近遇到了什么痛点问题？"
        )

    def call_evaluator(self, user_input):
        return (
            "【内容质检官 (Content Evaluator)】响应：\n"
            "正在执行110分双轨制体检...\n"
            "📊 [基础质量分]：85/100 (合格)\n"
            "🤖 [AI味检测分]：8/10 (人味较浓)\n"
            "💡 修改示范：..."
        )

    def call_channel_adapter(self, user_input):
        return (
            "【渠道分发专家 (Channel Adapter)】响应：\n"
            "正在为你执行平台适配排版...\n"
            "🔥 标题重构：...\n"
            "✅ 正文排版：[已增加 Emoji 并缩短段落]\n"
            "🖼️ 封面及互动建议：..."
        )

    def call_data_diagnoser(self, user_input):
        return (
            "【内容数据诊断师 (Data Diagnoser)】响应：\n"
            "正在读取化验单...\n"
            "🩺 病因诊断：完播率低，核心问题在「开头啰嗦，缺乏损失厌恶」。\n"
            "💊 迭代药方：修改前 vs 修改后对比..."
        )


class TestAgentEcosystemIO(unittest.TestCase):
    
    def setUp(self):
        self.system = MockAgentEcosystem()

    def test_01_router_compound_intent(self):
        """测试场景1：Router 复合意图调度 (打分及格后排版)"""
        res = self.system.execute("帮我看看这篇草稿，及格了直接排版成小红书")
        # 验证是否包含 Router 调度标记
        self.assertIn("[Router调度执行]", res)
        # 验证是否同时包含了评估和排版的输出结构
        self.assertIn("双轨制体检", res)
        self.assertIn("平台适配排版", res)

    def test_02_crafting_agent_io(self):
        """测试场景2：内容创作大师输入输出"""
        res = self.system.execute("想写篇关于职场内耗的文章，没灵感")
        self.assertIn("内容创作大师", res)
        self.assertIn("5步创作引导法", res)
        self.assertIn("选题阶段", res)

    def test_03_evaluator_agent_io(self):
        """测试场景3：内容质检官输入输出"""
        res = self.system.execute("帮我严格打分这篇草稿")
        self.assertIn("内容质检官", res)
        self.assertIn("基础质量分", res)
        self.assertIn("AI味检测分", res)

    def test_04_channel_adapter_agent_io(self):
        """测试场景4：渠道分发专家输入输出"""
        res = self.system.execute("把这篇文章改成小红书格式")
        self.assertIn("渠道分发专家", res)
        self.assertIn("Emoji", res)
        self.assertIn("标题重构", res)

    def test_05_data_diagnoser_agent_io(self):
        """测试场景5：数据诊断师输入输出"""
        res = self.system.execute("昨天的文章阅读量很低，帮我诊断一下数据")
        self.assertIn("内容数据诊断师", res)
        self.assertIn("病因诊断", res)
        self.assertIn("迭代药方", res)

if __name__ == '__main__':
    unittest.main(verbosity=2)
