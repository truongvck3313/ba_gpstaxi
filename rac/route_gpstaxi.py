import logging
import time
import var_gpstaxi
import module_other_gpstaxi
from login_gpstaxi import Login
from var_gpstaxi import imagepath, checklistpath
import asyncio
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import re







class Route:


    def __init__(self, page):
        self.page = page
        self.login_page = Login(page)


    async def Route(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        await self.page.click(f"xpath={var_gpstaxi.route}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_route}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.check_route, "Tốc độ", "_LoTrinh.png")


    async def Get_data(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_route}", timeout=500)
        except:
            await Route.Route(self, "", "", "")

        current_date = datetime.now()
        date_minus_1 = current_date - timedelta(days=1)
        date_str = date_minus_1.strftime("%d/%m/%Y")

        locator = self.page.locator(f"xpath={var_gpstaxi.FromDate}")
        await locator.press("Control+A")
        await locator.press("Backspace")
        await locator.fill(date_str)


        n = 0
        while (n < 6):
            n = n + 1
            path_vehicle = f"(//ul[contains(@id,'VehiclePlate_listbox')])[1]/li[{str(n)}]"
            await self.page.click(f"xpath={var_gpstaxi.route_select}")
            await asyncio.sleep(1.5)

            await self.page.click(f"xpath={path_vehicle}")
            await asyncio.sleep(1)

            await self.page.click(f"xpath={var_gpstaxi.btnGetData}")
            await asyncio.sleep(1.5)

            try:
                await self.page.click(f"xpath={var_gpstaxi.check_Get_data}", timeout=5000)
                await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Lộ trình - Tải dữ liệu",
                                                                              var_gpstaxi.check_Get_data, "", "_LoTrinh_TaiDuLieu.png")
                break
            except:
                if n == 5:
                    await self.page.screenshot(path=f"{imagepath}{code}_LoTrinh_TaiDuLieu.png", full_page=True)
                    module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                    module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_LoTrinh_TaiDuLieu.png")

        #
        # logging.info("Lộ trình - Tải dữ liệu")
        # logging.info(f"Mã - {code}")
        # logging.info(f"Tên sự kiện - {event}")
        # logging.info(f"Kết quả - {result}")
        # try:
        #     locator_list = self.page.locator(f"xpath={var_gpstaxi.check_Get_data}")
        #     list = await locator_list.inner_text()
        #     logging.info(f"list: {list}")
        #
        #     locator_map = self.page.locator(f"xpath={var_gpstaxi.scrollFix}")
        #     map = await locator_map.inner_text()
        #     logging.info(f"map: {map}")
        #     module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Popup lộ trình: {list}\nMap: {map}")
        #
        #     if (list != "") and (map != ""):
        #         logging.info("Pass")
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        #     else:
        #         logging.info("Fail")
        #         await self.page.screenshot(path=f"{imagepath}{code}_LoTrinh_TaiDuLieu.png", full_page=True)
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_LoTrinh_TaiDuLieu.png")
        # except Exception as e:
        #     logging.info(f"Fail - {e}")
        #     await self.page.screenshot(path=f"{imagepath}{code}_LoTrinh_TaiDuLieu.png", full_page=True)
        #     module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
        #     module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_LoTrinh_TaiDuLieu.png")


    async def Icon_config(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Get_data}", timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnSetting}")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Tải dữ liệu",
                                                                      var_gpstaxi.chkDisplayGenieEye_text, "Hiển thị mắt thần", "_LoTrinh_IconCauHinh.png")


    async def Config_text(self, code, event, result, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            try:
                await self.page.click(f"xpath={var_gpstaxi.btnSetting}", timeout=500)
                await asyncio.sleep(1.5)
            except:
                pass

        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Cấu hình -Checkbox",
                                                                      f"//*[@id='divConfig']//*[text()='{desire}']|"
                                                                      f"//*[@id='{desire}']/..", desire, name_image)


    async def Config_text1(self, code, event, result, path_name, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            try:
                await self.page.click(f"xpath={var_gpstaxi.btnSetting}", timeout=500)
                await asyncio.sleep(1.5)
            except:
                pass

        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Cấu hình -Checkbox",
                                                                      f"//*[@id='divConfig']//*[text()='{path_name}']|"
                                                                      f"//*[@id='{path_name}']/..", desire, name_image)


    async def Config_checkbox(self, code, event, result, path_checkbox, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            try:
                await self.page.click(f"xpath={var_gpstaxi.btnSetting}", timeout=500)
                await asyncio.sleep(1.5)
            except:
                pass

        checkbox = self.page.locator(path_checkbox)
        if not await checkbox.is_checked():
            await checkbox.click()
            await asyncio.sleep(1)


        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Cấu hình -Checkbox",
                                                                      f"//*[@id='routeReader']//*[text()='{desire}']", desire, name_image)

        await checkbox.click()
        await asyncio.sleep(1)


    async def Config_defaul(self, code, event, result, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.chkDisplayGenieEye}",  timeout=500)
        except:
            try:
                await self.page.click(f"xpath={var_gpstaxi.btnSetting}", timeout=500)
                await asyncio.sleep(1.5)
            except:
                pass

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Cấu hình -Checkbox",
                                                                      f"//*[@id='routeReader']//*[text()='{desire}']", desire, name_image)

        if name_image == "_LoTrinh_Popup_VGPS":
            await self.page.click(f"xpath={var_gpstaxi.btnSetting}")
            await asyncio.sleep(1.5)


    async def Icon_help(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Get_data}", timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnHelp}")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Lộ trình - Trợ giúp",
                                                                      var_gpstaxi.helpWindow_wnd_title, "Trợ Giúp", "_LoTrinh_TroGiup.png")

        await self.page.click(f"xpath={var_gpstaxi.helpWindow_wnd_title_x}")
        await asyncio.sleep(1.5)


    async def Check_icon(self, code, event, result, path_check, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Get_data}", timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await self.page.click(f"xpath={path_check}")
        await asyncio.sleep(1)

        if name_image == "_LoTrinh_IconRun":
            try:
                await self.page.wait_for_selector(f"xpath={path_check}", timeout=500)
            except:
                await self.page.click(f"xpath={var_gpstaxi.btnPause}")
                await asyncio.sleep(1.5)

        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Lộ trình - Check icon",
                                                                      path_check, name_image)


    async def Icon_print(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Get_data}", timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Lộ trình - Check icon",
                                                                    var_gpstaxi.btnPrint, var_gpstaxi.infoDiv,
                                                                    "Bản đồ lộ trình xe chạy", "_LoTrinh_In.png")


    async def Icon_excel(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Get_data}", timeout=500)
        except:
            await Route.Get_data(self, "", "", "")

        await module_other_gpstaxi.write_result_web_excel_dowload(self.page, code, event, result, "Lộ trình - Tải excel",
                                                                    var_gpstaxi.btnExcel, "_LoTrinh_Excel.png")








