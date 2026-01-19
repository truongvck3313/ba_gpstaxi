import asyncio
import warnings
from playwright.async_api import async_playwright
import time
from datetime import datetime
import module_other_gpstaxi
import var_gpstaxi
from caseid_gpstaxi import CaseID
import module_gpstaxi


# Giảm warnings ResourceWarning của asyncio/Windows
warnings.simplefilter("ignore", ResourceWarning)

# CASE_TO_RUN_chrome1 = [
#     # "Login01",
#     # "Login02",
#     # "Login03",
#     # "Login04",
#     # "Login05",
#     # "Login06",
#     # "Login07",
#     # "Login08",
#     # "Login09",
#     # "Login10",
#     # "Login11",
#     # "Login12",
#     # "Login13",
#     # "Login14",
#     # "Login15",
#     # "Login16",
#     # "Login17",
#     # "Login18",
#     # "Login19",
#     # "Login20",
#     # "Login21",
#     # "Login22",
#     # "Minitor01",
#     # "Minitor02",
#     # "Minitor03",
#     # "Minitor04",
#     # "Minitor05",
#     # "Minitor06",
#     # "Minitor07",
#     # "Minitor08",
#     # "Minitor09",
#     # "Minitor10",
#     # "Minitor11",
#     # "Minitor12",
#     # "Minitor13",
#     # "Minitor14",
#     # "Minitor15",
#     # "Minitor16",
#     # "Minitor17",
#     # "Minitor18",
#     # "Minitor19",
#     # "Minitor20",
#     # "Minitor21",
#     # "Minitor22",
#     # "Minitor23",
#     # "Minitor24",
#     # "Minitor25",
#     # "Minitor26",
#     # "Minitor27",
#     # "Minitor28",
#     # "Minitor29",
#     # "Minitor30",
#     # "Minitor31",
#     # "Minitor32",
#     # "Minitor33",
#     # "Minitor34",
#     # "Minitor35",
#     # "Minitor36",
#     # "Minitor37",
#     # "Minitor38",
#     # "Minitor39",
#     # "Minitor40",
#     # "Minitor41",
#     # "Minitor42",
#     # "Minitor43",
#     # "Minitor44",
#     # "Minitor45",
#     # "Minitor46",
#     # "Minitor47",
#     # "Minitor48",
#     # "Minitor49",
#     # "Minitor50",
#     # "Minitor51",
#     # "Minitor52",
#     # "Minitor53",
#     # "Minitor54",
#     # "Minitor55",
#     # "Minitor56",
#     # "Minitor57",
#     # "Minitor58",
#     # "Minitor59",
#     # "Minitor60",
#     # "Minitor61",
#     # "Minitor62",
#     # "Minitor63",
#     # "Minitor64",
#     # "Minitor65",
#     # "Minitor66",
#     # "Minitor67",
#     # "Minitor68",
#     # "Minitor69",
#     # "Minitor70",
#     # "Minitor71",
#     # "Minitor72",
#     # "Minitor73",
#     # "Minitor74",
#     # "Minitor75",
#     # "Minitor76",
#     # "Minitor77",
#     # "Minitor78",
#     # "Minitor79",
#     # "Minitor80",
#     # "Minitor81",
#     # "Minitor82",
#     # "Minitor83",
#     # "Minitor84",
#     # "Minitor85",
#     # "Minitor86",
#     # "Minitor87",
#     # "Minitor88",
#     # "Minitor89",
#     # "Minitor90",
#     # "Minitor91",
#     # "Minitor92",
#     # "Minitor93",
#     # "Minitor94",
#     # "Minitor95",
#     # "Minitor96",
#     # "Minitor97",
#     # "Minitor98",
#     # "Minitor99",
#     # "Minitor100",
#     # "Minitor101",
#     # "Minitor102",
#     # "Minitor103",
#     # "Minitor104",
#     # "Minitor105",
#     # "Minitor106",
#     # "Minitor107",
#     # "Minitor108",
#     # "Minitor109",
#     # "Minitor110",
#     # "Minitor111",
#     # "Minitor112",
#     # "Minitor113",
#     # "Minitor114",
#     # "Minitor115",
#     # "Minitor116",
#     # "Minitor117",
#     # "Minitor118",
#     # "Minitor119",
#     # "Minitor120",
#     # "Minitor121",
#     # "Minitor122",
#     # "Minitor123",
#     # "Minitor124",
#     # "Minitor125",
#     # "Minitor126",
#     # "Minitor127",
#     # "Minitor128",
#     # "Minitor129",
#     # "Minitor130",
#     # "Minitor131",
#     # "Minitor132",
#     # "Minitor133",
#     # "Minitor134",
#     # "Minitor135",
#     # "Minitor136",
#     # "Minitor137",
#     # "Minitor138",
#     # "Minitor139",
#     # "Minitor140",
#     # "Minitor141",
#     # "Minitor142",
#     # "Minitor143",
#     # "Minitor144",
#     # "Minitor145",
#     # "Minitor146",
#     # "Minitor147",
#     # "Minitor148",
#     # "Minitor149",
#     # "Minitor150",
#     # "Minitor151",
#     # "Minitor152",
#     # "Minitor153",
#     # "Minitor154",
#     # "Minitor155",
#     # "Minitor156",
#     # "Minitor157",
#     # "Minitor158",
#     # "Minitor159",
#     # "Minitor160",
#     # "Minitor161",
#     # "Minitor162",
#     # "Minitor163",
#     # "Minitor164",
#     # "Minitor165",
#     # "Minitor166",
#     # "Minitor167",
#     # "Minitor168",
#     # "Minitor169",
#     # "Minitor170",
#     # "Minitor171",
#     # "Minitor172",
#     # "Minitor173",
#     # "Minitor174",
#     # "Minitor175",
#     # "Minitor176",
#     # "Minitor177",
#     # "Minitor178",
#     # "Minitor179",
#     # "Minitor180",
#     # "Minitor181",
#     # "Minitor182",
#     # "Minitor183",
#     # "Minitor184",
#     # "Minitor185",
#     # "Minitor186",
#     # "Minitor187",
#     # "Minitor188",
#     # "Minitor189",
#     # "Minitor190",
#     # # "Minitor191",
#     # # "Minitor192",
#     # # "Minitor193",
#     # # "Minitor194",
#     # # "Minitor195",
#     # # "Minitor196",
#     # # "Minitor197",
#     # # "Minitor198",
#     # # "Minitor199",
#     # # "Minitor200",
#     # # "Minitor201",
#     # # "Minitor202",
#     # # "Minitor203",
#     # # "Minitor204",
#     # "Minitor205",
#     # "Minitor206",
#     # "Minitor207",
#     # "Minitor208",
#     # "Minitor209",
#     # "Minitor210",
#     # "Minitor211",
#     # "Minitor212",
#     # "Minitor213",
#     # "Minitor214",
#     # "Minitor215",
#     # "Minitor216",
#     # "Minitor217",
#     # "Minitor218",
#     # "Minitor219",
#     # "Minitor220",
#     # "Minitor221",
#     # "Minitor222",
#     # "Minitor223",
#     # "Minitor224",
#     # "Minitor225",
#     # "Minitor226",
#     # "Minitor227",
#     # "Minitor228",
#     # "Minitor229",
#     # "Minitor230",
#     # "Route01",
#     # "Route02",
#     # "Route03",
#     # "Route04",
#     # "Route05",
#     # "Route06",
#     # "Route07",
#     # "Route08",
#     # "Route09",
#     # "Route10",
#     # "Route11",
#     # "Route12",
#     # "Route13",
#     # "Route14",
#     # "Route15",
#     # "Route16",
#     # "Route17",
#     # "Route18",
#     # "Route19",
#     # "Route20",
#     # "Route21",
#     # "Route22",
#     # "Route23",
#     # "Route24",
#     # "Report01",
#     # "Report02",
#     # "Report03",
#     # "Report04",
#     # "Report05",
#     # "Report06",
#     # "Report07",
#     # "Report08",
#     # "Report09",
#     # "Report10",
#     # "Report11",
# ]
#
#
# CASE_TO_RUN_chrome2 = [
#     # "Login01",
#     # "Login02",
#     # "Login03",
#     # "Login04",
#     # "Login05",
#     # "Login06",
#     # "Login07",
#     # "Login08",
#     # "Login09",
#     # "Login10",
#     # "Login11",
#     # "Login12",
#     # "Login13",
#     # "Login14",
#     # "Login15",
#     # "Login16",
#     # "Login17",
#     # "Login18",
#     # "Login19",
#     # "Login20",
#     # "Login21",
#     # "Login22",
#     # "Minitor01",
#     # "Minitor02",
#     # "Minitor03",
#     # "Minitor04",
#     # "Minitor05",
#     # "Minitor06",
#     # "Minitor07",
#     # "Minitor08",
#     # "Minitor140",
#     # "Minitor154",
#     # "Minitor155",
#     # "Minitor195",
#     # "Minitor196",
#     # "Minitor197",
#     # "Minitor198",
#     # "Route19",
# ]
#
#
# CASE_TO_RUN_chrome3 = [
#     # "Login01",
#     # "Login02",
#     # "Login03",
#     # "Login04",
#     # "Login05",
#     # "Login06",
#     # "Login07",
#     # "Login08",
#     # "Login09",
#     # "Login10",
#     # "Login11",
#     # "Login12",
#     # "Login13",
#     # "Login14",
#     # "Login15",
#     # "Login16",
#     # "Login17",
#     # "Login18",
#     # "Login19",
#     # "Login20",
#     # "Login21",
#     # "Login22",
#     # "Minitor01",
#     # "Minitor02",
#     # "Minitor03",
#     # "Minitor04",
#     # "Minitor05",
#     # "Minitor06",
#     # "Minitor07",
#     # "Minitor08",
# ]



# chrome 1
CASE_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon()
RETEST_CASE_NONE_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon_retest_none()
RETEST_CASE_FAIL_TO_RUN_chrome1 = module_gpstaxi.Login_Minitor_icon_retest_fail()

muc1_thuong = module_gpstaxi.Login_Minitor_icon()
muc1_trong = module_gpstaxi.Login_Minitor_icon_retest_none()
muc1_fail = module_gpstaxi.Login_Minitor_icon_retest_fail()
# print(f"muc1_thuong: {muc1_thuong}")
# print(f"muc1_trong: {muc1_trong}")
# print(f"muc1_fail: {muc1_fail}")


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

    # Chrome 1
    tasks.append(run_chrome(playwright, "Profile 30", CASE_TO_RUN_chrome1, RETEST_CASE_NONE_TO_RUN_chrome1,
            RETEST_CASE_FAIL_TO_RUN_chrome1, "Chrome 1", report))

    # Chrome 2
    tasks.append(run_chrome(playwright, "Profile 31", CASE_TO_RUN_chrome2, RETEST_CASE_NONE_TO_RUN_chrome2,
            RETEST_CASE_FAIL_TO_RUN_chrome2, "Chrome 2", report))

    # Chrome 3
    tasks.append(run_chrome(playwright, "Profile 32", CASE_TO_RUN_chrome3, RETEST_CASE_NONE_TO_RUN_chrome3,
            RETEST_CASE_FAIL_TO_RUN_chrome3, "Chrome 3", report))

    # Chrome 4
    tasks.append(run_chrome(playwright, "Profile 33", CASE_TO_RUN_chrome4, RETEST_CASE_NONE_TO_RUN_chrome4,
            RETEST_CASE_FAIL_TO_RUN_chrome4,"Chrome 4", report))



    # # Chrome debug 1
    # tasks.append(run_chrome_debug(playwright, "Profile 30", CASE_TO_RUN_chrome1, "Chrome 1", report))
    # # Chrome debug 2
    # tasks.append(run_chrome_debug(playwright, "Profile 31", CASE_TO_RUN_chrome2, "Chrome 2", report))


    # 🔥 CHẠY SONG SONG THẬT SỰ
    # code chạy
    module_other_gpstaxi.clearData(var_gpstaxi.checklistpath, "Checklist", "", "", "")
    module_other_gpstaxi.clear_log()
    module_other_gpstaxi.delete_image()
    module_other_gpstaxi.timerun()
    await asyncio.gather(*tasks)
    await playwright.stop()
    module_other_gpstaxi.send_viber()

    print("✅ Tất cả Chrome đã chạy xong.")
    module_other_gpstaxi.print_final_report(report, test_start_time)




loop = asyncio.get_event_loop()
loop.run_until_complete(main())