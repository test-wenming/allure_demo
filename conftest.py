
import allure
import pytest
from selenium import webdriver
from py.xml import html
# import time
# from lib.qq_email import email


# _driver = None
# 测试失败时添加截图和测试用例描述(用例的注释信息)
caseNum2Row = {}     # 用例编号->行数 表
TEST_RET_COL_NO = 4  # 测试结果在用例excel文件中的列数


# 修改@pytest.mark.parametrize的参数名（code）为Excel中的用例编号，再通过report.nodeid获取该用例编号。
def pytest_make_parametrize_id(val):
    newid = str(val[0])
    return newid


@pytest.mark.hookwrapper(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):

    """当测试失败的时候，自动截图，展示到html报告中"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    # print('这个是用例描述description:%s' % str(item.function.__doc__))

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
    report.description = str(item.function.__doc__)

    print(f'用例步骤：{report.when},用例结果：{report.outcome}')

    # if report.when == "call":
    #     getCaseNum2RowInExcel()
    #     import win32com.client
    #     excel = win32com.client.Dispatch("Excel.Application")
    #     excel.Visible = True
    #     workbook = excel.Workbooks.Open(r'C:\Users\Administrator\Desktop\login.xlsx')
    #     sheet = workbook.Sheets(1)
    #
    #     # 初衷是想通过 key, value 的方式 set get 获取用例编号
    #     # code_value = item.config.cache.get(str(code), None)
    #     # caseNo = code_value
    #
    #     # 找到对应的测试用例在excel中的行数
    #     print(f'这个是report.nodeid：{report.nodeid}')
    #     code = report.nodeid.split("[")[-1][:-1]
    #     cell = sheet.Cells(caseNum2Row[code], TEST_RET_COL_NO)
    #     # 翻动滚动条，保证当前测试结果单元格可见
    #     # excel.ActiveWindow.ScrollRow = caseNum2Row[caseNo] - 2
    #
    #     if report.outcome == 'passed':
    #         cell.Value = 'passed'
    #         cell.Font.Color = 0xBF00  # 设置为绿色
    #
    #     else:
    #         cell.Font.Color = 0xFF  # 设置为红色
    #         if report.outcome == 'failed':
    #             cell.Value = 'failed'
    #         else:
    #             cell.Value = 'error'
    #     # 保存内容
    #     workbook.Save()


def pytest_terminal_summary(terminalreporter, exitstatus, config):

    total_case = terminalreporter._numcollected
    pass_case = len([i for i in terminalreporter.stats.get('passed', [])])
    fail_case = len([i for i in terminalreporter.stats.get('failed', [])])
    error_case = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skip_case = len([i for i in terminalreporter.stats.get('skipped', [])])
    pass_rate = round(pass_case / total_case * 100, 2)

    desc = """
    本次执行情况如下：
    总用例数为：{}
    通过用例数：{}
    失败用例数：{}
    错误用例数：{}
    跳过用例数：{}
    通过率为： {} %
    """.format(total_case, pass_case, fail_case, error_case, skip_case, pass_rate)

    print(desc)
    # try:
    #     email.send_file('1598253873@qq.com', desc, '自动化用例执行结果',
    #                     r'C:\Users\Administrator\PycharmProjects\pytest_Allure_Excel\cases\html-report\report.html',
    #                     'html测试报告.html')
    #     print('邮件发送成功！！！')
    #
    # except:
    #     print('邮件发送失败！！！')


def getCaseNum2RowInExcel():
    """
    得到Excel 中用例 编号对应的行数，方便填写测试结果
    """
    import xlrd
    book = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\login.xlsx')
    sheet = book.sheet_by_index(0)
    caseNumbers = sheet.col_values(colx=0)

    for row, cn in enumerate(caseNumbers):
        if '-' in cn:
            caseNum2Row[cn] = row + 1


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    print("########################这是pytest_html_results_table_header函数#############################################")
    cells.insert(1, html.th('Description'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    print("########################这是pytest_html_results_table_row函数#############################################")
    cells.insert(1, html.td(report.description))


def _capture_screenshot():
    allure.attach(
        _driver.get_screenshot_as_png(),
        "失败截图",
        allure.attachment_type.PNG
    )
    '''截图保存为base64'''
    return _driver.get_screenshot_as_base64()


@pytest.fixture()
def driver():
    print("########################这是driver函数#############################################")
    global _driver
    print('------------open browser------------')
    _driver = webdriver.Chrome()
    _driver.maximize_window()

    yield _driver

    print('------------close browser------------')
    _driver.quit()









