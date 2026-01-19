import asyncio
import warnings
from playwright.async_api import async_playwright
import time
from datetime import datetime
import module_other_gpstaxi
import var_gpstaxi
from caseid_gpstaxi import CaseID
import module_gpstaxi


warnings.simplefilter("ignore", ResourceWarning)

CASE_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon()
RETEST_CASE_NONE_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon_retest_none()
RETEST_CASE_FAIL_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon_retest_fail()

muc1_thuong = module_gpstaxi.Login_Minitor_icon()
muc1_trong = module_gpstaxi.Login_Minitor_icon_retest_none()

#chrome 2
CASE_TO_RUN_chrome2 = module_gpstaxi.Minitor_list_vehicle()
RETEST_CASE_NONE_TO_RUN_chrome2 = module_gpstaxi.Minitor_list_vehicle_retest_none()
RETEST_CASE_FAIL_TO_RUN_chrome2 = module_gpstaxi.Minitor_list_vehicle_retest_fail()


#chrome 3
CASE_TO_RUN_chrome3 = module_gpstaxi.Minitor_right_Vehicle_Map()
RETEST_CASE_NONE_TO_RUN_chrome3 = module_gpstaxi.Minitor_right_Vehicle_Map_retest_none()
RETEST_CASE_FAIL_TO_RUN_chrome3 = module_gpstaxi.Minitor_right_Vehicle_Map_retest_fail()


#Chrome4
CASE_TO_RUN_chrome4 = module_gpstaxi.Monitor_multiple_Route_Report()
RETEST_CASE_NONE_TO_RUN_chrome4 = module_gpstaxi.Monitor_multiple_Route_Report_retest_none()
RETEST_CASE_FAIL_TO_RUN_chrome4 = module_gpstaxi.Monitor_multiple_Route_Report_retest_fail()












async def run_cases_on_page(page, case_list, chrome_name, report):
    """Chạy case + lưu thời gian chạy vào report"""
    case_instance = CaseID(page)

    chrome_start = time.time()

    report[chrome_name] = {
        "cases": [],
        "total_time": 0
    }

    for func_name in case_list:
        case_start = time.time()
        start_dt = datetime.now().strftime("%H:%M:%S")

        try:
            print(f"[{start_dt}] [{chrome_name}] Bắt đầu case: {func_name}")
            await getattr(case_instance, func_name)()

            case_end = datetime.now().strftime("%H:%M:%S")
            elapsed = time.time() - case_start

            print(f"[{case_end}] [{chrome_name}] Case {func_name} hoàn tất ({elapsed:.2f}s)")

            report[chrome_name]["cases"].append({
                "name": func_name,
                "status": "PASS",
                "time": elapsed
            })

        except Exception as e:
            case_end = datetime.now().strftime("%H:%M:%S")
            elapsed = time.time() - case_start

            print(f"[{case_end}] [{chrome_name}] Case {func_name} lỗi: {e} ({elapsed:.2f}s)")

            report[chrome_name]["cases"].append({
                "name": func_name,
                "status": "FAIL",
                "time": elapsed
            })

    report[chrome_name]["total_time"] = time.time() - chrome_start



async def run_chrome_debug(playwright, profile_name, page_cases, chrome_name, report):
    chrome = await playwright.chromium.launch_persistent_context(
        user_data_dir=f"{var_gpstaxi.chromeuser}{profile_name}",
        headless=False,
        accept_downloads=True,
        viewport={'width': 1920, 'height': 910},
        args=[
            "--window-position=0,0",
            "--window-size=1920,1080",
            "--disable-blink-features=AutomationControlled",
            "--disable-features=AutomationControlled"])

    page = chrome.pages[0] if chrome.pages else await chrome.new_page()

    try:
        if page_cases:
            await run_cases_on_page(page, page_cases, chrome_name, report)
        else:
            print(f"⚠️ {chrome_name} không có case nào.")
    finally:
        await asyncio.sleep(5)
        print(f"🔒 Đóng {chrome_name}")
        await chrome.close()



async def run_chrome_none_fail(playwright, profile_name, retest_none_cases, retest_fail_cases, chrome_name, report):
    chrome = await playwright.chromium.launch_persistent_context(
        user_data_dir=f"{var_gpstaxi.chromeuser}{profile_name}",
        headless=False,
        accept_downloads=True,
        viewport={'width': 1920, 'height': 910},
        args=[
            "--window-position=0,0",
            "--window-size=1920,1080",
            "--disable-blink-features=AutomationControlled",
            "--disable-features=AutomationControlled"])

    page = chrome.pages[0] if chrome.pages else await chrome.new_page()

    try:
        if retest_none_cases:
            await run_cases_on_page(page, retest_none_cases, chrome_name, report)

        if retest_fail_cases:
            await run_cases_on_page(page, retest_fail_cases, chrome_name, report)
        else:
            print(f"⚠️ {chrome_name} không có case nào.")
    finally:
        print(f"🔒 Đóng {chrome_name}")
        await chrome.close()



async def run_chrome(playwright, profile_name, page_cases, retest_none_cases, retest_fail_cases, chrome_name, report):
    chrome = await playwright.chromium.launch_persistent_context(
        user_data_dir=f"{var_gpstaxi.chromeuser}{profile_name}",
        headless=False,
        accept_downloads=True,
        viewport={'width': 1920, 'height': 910},
        args=[
            "--window-position=0,0",
            "--window-size=1920,1080",
            "--disable-blink-features=AutomationControlled",
            "--disable-features=AutomationControlled"])

    page = chrome.pages[0] if chrome.pages else await chrome.new_page()

    try:
        if page_cases:
            await run_cases_on_page(page, page_cases, chrome_name, report)

            if retest_none_cases:
                await run_cases_on_page(page, retest_none_cases, chrome_name, report)

            if retest_fail_cases:
                await run_cases_on_page(page, retest_fail_cases, chrome_name, report)
        else:
            print(f"⚠️ {chrome_name} không có case nào.")
    finally:
        print(f"🔒 Đóng {chrome_name}")
        await chrome.close()






async def main():
    test_start_time = time.time()
    report = {}
    playwright = await async_playwright().start()
    tasks = []

    # -------------FULL LUỒNG-----------------
    tasks.append(run_chrome(playwright, "Profile 30", CASE_TO_RUN_chrome1, RETEST_CASE_NONE_TO_RUN_chrome1,
            RETEST_CASE_FAIL_TO_RUN_chrome1, "Chrome 1", report))

    tasks.append(run_chrome(playwright, "Profile 31", CASE_TO_RUN_chrome2, RETEST_CASE_NONE_TO_RUN_chrome2,
            RETEST_CASE_FAIL_TO_RUN_chrome2, "Chrome 2", report))

    tasks.append(run_chrome(playwright, "Profile 32", CASE_TO_RUN_chrome3, RETEST_CASE_NONE_TO_RUN_chrome3,
            RETEST_CASE_FAIL_TO_RUN_chrome3, "Chrome 3", report))

    tasks.append(run_chrome(playwright, "Profile 33", CASE_TO_RUN_chrome4, RETEST_CASE_NONE_TO_RUN_chrome4,
            RETEST_CASE_FAIL_TO_RUN_chrome4,"Chrome 4", report))


    #-------------DEBUG-----------------
    # tasks.append(run_chrome_debug(playwright, "Profile 30", CASE_TO_RUN_chrome1, "Chrome 1", report))
    # tasks.append(run_chrome_debug(playwright, "Profile 31", CASE_TO_RUN_chrome2, "Chrome 2", report))




    # #-------------NONE- FAIL-----------------
    # tasks.append(run_chrome_none_fail(playwright, "Profile 30", RETEST_CASE_NONE_TO_RUN_chrome1,
    #         RETEST_CASE_FAIL_TO_RUN_chrome1, "Chrome 1", report))
    #
    # tasks.append(run_chrome_none_fail(playwright, "Profile 31", RETEST_CASE_NONE_TO_RUN_chrome2,
    #         RETEST_CASE_FAIL_TO_RUN_chrome2, "Chrome 2", report))
    #
    # tasks.append(run_chrome_none_fail(playwright, "Profile 32", RETEST_CASE_NONE_TO_RUN_chrome3,
    #         RETEST_CASE_FAIL_TO_RUN_chrome3, "Chrome 3", report))
    #
    # tasks.append(run_chrome_none_fail(playwright, "Profile 33", RETEST_CASE_NONE_TO_RUN_chrome4,
    #         RETEST_CASE_FAIL_TO_RUN_chrome4,"Chrome 4", report))



    # 🔥 CHẠY SONG SONG THẬT SỰ
    # code chạy
    day = 0
    while True:
        module_other_gpstaxi.timerun()
        day += 1
        module_other_gpstaxi.clearData(var_gpstaxi.checklistpath, "Checklist", "", "", "")
        module_other_gpstaxi.clear_log()
        module_other_gpstaxi.delete_image()
        module_other_gpstaxi.timerun()
        await asyncio.gather(*tasks)
        await playwright.stop()
        module_other_gpstaxi.send_viber()
        print("✅ Tất cả Chrome đã chạy xong.")
        module_other_gpstaxi.print_final_report(report, test_start_time)


        print("đang chạy ngày thứ n: ", day)
        if day == 7:
            module_other_gpstaxi.clear_log()
            day = 0











loop = asyncio.get_event_loop()
loop.run_until_complete(main())