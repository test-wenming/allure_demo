import xlrd
import allure
import pytest
import ddddocr
import os

# lines = []  # 创建空表用来存Excel每一行内容
# worksheet = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\login.xlsx').sheet_by_index(0)
# rows = worksheet.nrows  # 获取行数
# for i in range(1, rows):
#     line = worksheet.row_values(i)
#     line2 = [str(li).split('.')[0] for li in line]
#     lines.append(line2)
#
#
# @pytest.fixture(params=lines)  # pytest工厂函数，默认方法级别
# def init_x(request):
#     return request.param  # 固定格式，每一次取出params的一个元素
#
#
# @allure.feature("测试模块描述")
# class Test_Login:
#     @allure.story("登录1")
#     def test_UI_0001(self,driver,init_x):
#
#         print("########################这是用例函数#############################################")
#
#         _driver = driver
#         _driver.get('https://piikmall.com/mall/index.php?act=seller_login')
#         _driver.implicitly_wait(10)
#         _driver.find_element_by_css_selector(".item #user_name").clear()
#         _driver.find_element_by_css_selector(".item #user_name").send_keys(init_x[1])
#
#         _driver.find_element_by_css_selector("#password").clear()
#         _driver.find_element_by_css_selector("#password").send_keys(init_x[2])
#
#         _driver.find_element_by_css_selector("#captcha").clear()
#         _driver.find_element_by_css_selector("#captcha").send_keys(init_x[3])
#
#         _driver.find_element_by_css_selector("#loginsubmit").click()
#
#         a = _driver.find_element_by_css_selector("#fwin_dialog > div.eject_con > div").text
#
#
#         assert a == "Login successful"


def get_data():

    lines = []  # 创建空表用来存Excel每一行内容
    worksheet = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\login.xlsx').sheet_by_index(0)
    rows = worksheet.nrows  # 获取行数
    for i in range(1, rows):
        line = worksheet.row_values(i)
        line2 = [str(li).split('.')[0] for li in line]
        lines.append(line2)
    return lines


@allure.feature("测试登录模块")
class Test_Login:

    @classmethod
    def setup_class(cls):
        print('\n === 初始化-类 ===')

    @classmethod
    def teardown_class(cls):
        print('\n === 清除 - 类 ===')

    @pytest.mark.parametrize("code", get_data())  # pytest参数化装饰器，第一个参数写自定义的参数名，第二个参数传取到的数据
    @allure.story("测试登录")
    @allure.step("1、输入用户名 \n 2、输入密码  \n 3、提交登录")
    def test_UI_0001(self, driver, code, cache):

        # 初衷是想通过 key, value 的方式 set get 获取用例编号
        # cache.set(key=str(code[0]), value=code[0])

        print("########################这是用例函数#############################################")

        _driver = driver
        _driver.get('https://piikmall.com/mall/index.php?act=seller_login')
        _driver.implicitly_wait(10)

        _driver.find_element_by_css_selector(".item #user_name").clear()
        _driver.find_element_by_css_selector(".item #user_name").send_keys(code[1])

        _driver.find_element_by_css_selector("#password").clear()
        _driver.find_element_by_css_selector("#password").send_keys(code[2])

        _driver.find_element_by_css_selector("#captcha").clear()
        # 获取图片验证码
        driver.find_element_by_css_selector('.item #codeimage').screenshot('code.png')
        # 以下为识别验证码的代码
        ocr = ddddocr.DdddOcr()
        with open("code.png", "rb") as fp:
            image_code = fp.read()
        catch = ocr.classification(image_code)  # 验证码返回给catch
        os.remove('code.png')

        _driver.find_element_by_css_selector("#captcha").send_keys(catch)

        _driver.find_element_by_css_selector("#loginsubmit").click()

        a = _driver.find_element_by_css_selector("#fwin_dialog > div.eject_con > div").text
        assert a == "Login successful"


# 如果要生成pytest-html报告，文件-设置-Python 集成工具-默认测试运行程序-改成Unittest
# 否则在根目录使用终端命令运行：pytest cases/login --capture=sys --html=cases/html-report/report.html --self-contained-html
if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_login.py', '--capture=sys', '--html=../html-report/report.html', '--self-contained-html'])









