import os
import sys
import unittest
import shutil
import tempfile
from unittest.mock import patch, MagicMock

# 添加父目录到Python路径以导入main模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

class TestVirtualEnvironment(unittest.TestCase):
    def setUp(self):
        # 创建临时目录用于测试
        self.test_dir = tempfile.mkdtemp()
        self.venv_name = "test_venv"
        self.venv_path = os.path.join(self.test_dir, self.venv_name)

    def tearDown(self):
        # 清理临时目录
        shutil.rmtree(self.test_dir)

    def test_get_python_executable(self):
        # 测试获取Python可执行文件路径
        python_path = main.get_python_executable()
        self.assertTrue(os.path.exists(python_path))
        self.assertTrue('python' in python_path.lower())

    @patch('subprocess.run')
    def test_check_venv_health_healthy(self, mock_run):
        # 模拟健康的虚拟环境
        mock_run.return_value = MagicMock(returncode=0)
        os.makedirs(os.path.dirname(main.get_venv_python(self.venv_path)), exist_ok=True)
        
        is_healthy, message = main.check_venv_health(self.venv_path)
        self.assertTrue(is_healthy)
        self.assertEqual(message, "虚拟环境正常")

    @patch('subprocess.run')
    def test_check_venv_health_unhealthy(self, mock_run):
        # 模拟不健康的虚拟环境
        mock_run.return_value = MagicMock(returncode=1, stderr="Import Error")
        os.makedirs(os.path.dirname(main.get_venv_python(self.venv_path)), exist_ok=True)
        
        is_healthy, message = main.check_venv_health(self.venv_path)
        self.assertFalse(is_healthy)
        self.assertTrue("依赖包导入失败" in message)

    @patch('subprocess.check_call')
    @patch('main.check_venv_health')
    def test_create_or_get_venv_new(self, mock_check_health, mock_check_call):
        # 测试创建新的虚拟环境
        venv_path, is_new = main.create_or_get_venv(self.venv_name)
        self.assertTrue(is_new)
        mock_check_call.assert_called_once()

    @patch('subprocess.check_call')
    @patch('main.check_venv_health')
    def test_create_or_get_venv_existing_healthy(self, mock_check_health, mock_check_call):
        # 测试使用现有的健康虚拟环境
        os.makedirs(self.venv_path)
        mock_check_health.return_value = (True, "虚拟环境正常")
        
        venv_path, is_new = main.create_or_get_venv(self.venv_name)
        self.assertFalse(is_new)
        mock_check_call.assert_not_called()

    @patch('subprocess.check_call')
    @patch('main.check_venv_health')
    def test_create_or_get_venv_existing_unhealthy(self, mock_check_health, mock_check_call):
        # 测试重新创建不健康的虚拟环境
        os.makedirs(self.venv_path)
        mock_check_health.return_value = (False, "依赖包导入失败")
        
        venv_path, is_new = main.create_or_get_venv(self.venv_name)
        self.assertTrue(is_new)
        mock_check_call.assert_called_once()

    @patch('subprocess.Popen')
    @patch('main.create_or_get_venv')
    def test_main_success(self, mock_create_venv, mock_popen):
        # 测试主函数成功执行
        mock_create_venv.return_value = (self.venv_path, False)
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process
        
        result = main.main()
        self.assertEqual(result, 0)

    @patch('subprocess.Popen')
    @patch('main.create_or_get_venv')
    def test_main_failure(self, mock_create_venv, mock_popen):
        # 测试主函数失败情况
        mock_create_venv.return_value = (self.venv_path, False)
        mock_process = MagicMock()
        mock_process.poll.return_value = 1
        mock_process.communicate.return_value = ("", "Error")
        mock_popen.return_value = mock_process
        
        result = main.main()
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main() 