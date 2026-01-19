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

logging.basicConfig(
    handlers=[logging.FileHandler(filename=var_gpstaxi.logpath, encoding='utf-8', mode='a+')],
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%F %A %T",
    level=logging.INFO
)


async def get_info_status(page, field, row):
    n = 1
    while (n < 30):
        n = n + 1
        path_name = f"//*[@id='tab1']/div[2]/div[{str(n)}]/div[1]"
        path_data = f"//*[@id='tab1']/div[2]/div[{str(n)}]/div[2]"
        path_check = f"//*[@id='tab1']/div[2]/div[{str(n)}]"
        try:
            name = await page.locator(f"xpath={path_check}").inner_text(timeout=200)
        except:
            break

        try:
            name = await page.locator(f"xpath={path_name}").inner_text(timeout=200)
            data = await page.locator(f"xpath={path_data}").inner_text(timeout=200)
            print(f"Dòng: {n}, {name}: {data}")
            if name == field:
                var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", row, 2, data)
                break
        except:
            pass


async def get_info_bgt(page, field, row):
    n = 0
    while (n < 15):
        n = n + 1
        path_name = f"//*[@id='tab2']/div[{str(n)}]/div[1]"
        path_data = f"//*[@id='tab2']/div[{str(n)}]/div[2]"
        try:
            name = await page.locator(f"xpath={path_name}").inner_text(timeout=200)
            data = await page.locator(f"xpath={path_data}").inner_text(timeout=200)
            print(f"Dòng: {n}, {name}: {data}")
            if name == field:
                var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", row, 2, data)
                break
        except:
            pass








class IconPage:

    def __init__(self, page):
        self.page = page  # Page Playwright async
        self.login_page = Login(page)  # Dùng Login async


    async def icon_zoom(self, code, event, result, path_icon, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={path_icon}", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={path_icon}")
        await self.page.wait_for_timeout(1000)
        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result,
                                                          "Giám sát - Icon", path_icon, name_image)


    async def select_map(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.Layers}", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        # await self.page.click(f"xpath={var_gpstaxi.Layers}")
        button = self.page.locator(f"xpath={var_gpstaxi.Layers}")
        await button.wait_for(state="attached", timeout=1500)
        await button.wait_for(state="visible", timeout=1500)
        await button.scroll_into_view_if_needed()
        await button.hover(force=True, timeout=1500)
        await asyncio.sleep(1.5)

        logging.info("Giám sát - Icon")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            name_Layers1 = await self.page.locator(f"xpath={var_gpstaxi.name_Layers1}").inner_text()
            name_Layers2 = await self.page.locator(f"xpath={var_gpstaxi.name_Layers2}").inner_text()
            name_Layers3 = await self.page.locator(f"xpath={var_gpstaxi.name_Layers3}").inner_text()

            logging.info(f"name_Layers1: {name_Layers1}\nname_Layers2: {name_Layers2}\nname_Layers3: {name_Layers3}\n")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{name_Layers1}, {name_Layers2}, {name_Layers3}")

            if (name_Layers1 == " Bình Anh") and (name_Layers2 == " Bản đồ") and (name_Layers3 == " Vệ tinh"):
                logging.info("Pass")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_IconPhongTo.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_IconPhongTo.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_IconPhongTo.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_IconPhongTo.png")





    async def c08_bca(self, code, event, result):
        await self.login_page.goto("Mã XN", "423", "DNTN Quỳnh Hoa [423]")

        await self.page.click(f"xpath={var_gpstaxi.c08_bca}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                var_gpstaxi.panelMissingInfomationBca_wnd_title, "Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                "_GiamSat_DanhSachCanhBaoTruyenC08BCA.png")


    async def c08_bca_link(self, code, event, result, link, path_check, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                link, path_check, desire, name_image)


    async def c08_bca_refresh(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        await module_other_gpstaxi.write_result_status_code(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                var_gpstaxi.icon_refresh, "/Online/GetAllDataBcaMissingInfo",  "_DanhSachCanhBaoTruyenC08BCA_IconLamMoi.png")


    async def c08_bca_group(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.c08_bca_group}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.c08_bca_group2}")

        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                var_gpstaxi.c08_bca_group2, "",  "_DanhSachCanhBaoTruyenC08BCA_NhomPhuongTien.png")


    async def c08_bca_vehicle(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        number2 = await self.page.locator(f"xpath={var_gpstaxi.list_bca_2_2}").inner_text()
        vehicle2 = await self.page.locator(f"xpath={var_gpstaxi.list_bca_2_3}").inner_text()

        await self.page.click(f"xpath={var_gpstaxi.c08_bca_vehicle}")

        await self.page.fill(f"xpath={var_gpstaxi.c08_bca_vehicle_input}", vehicle2)

        await self.page.click(f"xpath=(//div[contains(@class,'ms-parent')])[2]/div/ul//*[text()=' {number2} - {vehicle2}']")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                var_gpstaxi.list_bca_1_3, vehicle2,  "_DanhSachCanhBaoTruyenC08BCA_PhuongTien.png")

        await self.page.click(f"xpath={var_gpstaxi.c08_bca_vehicle1}")
        await self.page.click(f"xpath={var_gpstaxi.icon_refresh}")


    async def c08_bca_check_info(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        logging.info("Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            stt = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_1}").inner_text()
            number = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_2}").inner_text()
            liscens_plate = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_3}").inner_text()
            conten = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_4}").inner_text()
            day = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_5}").inner_text()
            person = await self.page.locator(f"xpath={var_gpstaxi.list_bca_1_6}").inner_text()

            logging.info(f"STT: {stt}\nSố hiệu xe: {number}\nBiển số xe: {liscens_plate}\n"
                         f"Nội dung cảnh báo: {conten}\nNgày bỏ tích truyền: {day}\nNgười bỏ tích truyền: {person}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"STT: {stt}\nSố hiệu xe: {number}\nBiển số xe: {liscens_plate}\n"
                         f"Nội dung cảnh báo: {conten}\nNgày bỏ tích truyền: {day}\nNgười bỏ tích truyền: {person}")

            if (stt == "1") and (number != "") and (liscens_plate != "") and (conten != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_C08BCA_CheckThongTin.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_C08BCA_CheckThongTin.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_C08BCA_CheckThongTin.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")


    async def c08_bca_icon_transmission(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                    var_gpstaxi.list_bca_1_7_a, var_gpstaxi.check_c08_vehicle, "Loại hình kinh doanh",
                                                                    "_DanhSachCanhBaoTruyenC08BCA_ThongTinLaiXe.png")


    async def c08_bca_displayed(self, code, event, result, checkbox, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                    checkbox, name_image)


    async def c08_bca_close(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}",  timeout=500)
        except:
            await IconPage.c08_bca(self, "", "", "")

        await module_other_gpstaxi.write_result_close(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                    var_gpstaxi.close_missing, "_C08BCA_Dong.png")





    async def hidden_car_list(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.vehiclesHiddenWindow_wnd_title}")

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.vehiclesHiddenWindow_wnd_title, "Danh sách xe đang ẩn",
                                                                "_GiamSat_DanhSachXeDangAn.png")


    async def hidden_car_list_add_new(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnAddVehicleHidden}")
        await asyncio.sleep(2)
        await self.page.type(f"xpath={var_gpstaxi.acVehicleHiddenVehicle}", var_gpstaxi.data['minitor']['hide_vehicle'])
        await self.page.click(f"xpath={var_gpstaxi.btnAddVehicleHidden1}")
        await self.page.click(f"xpath={var_gpstaxi.radHideTrackingAdd}")
        await self.page.click(f"xpath={var_gpstaxi.radStopTransferAdd}")
        await self.page.click(f"xpath={var_gpstaxi.btnAddVehicleHidden_resson}")
        await self.page.click(f"xpath={var_gpstaxi.btnAddVehicleHidden_resson1}")
        await self.page.type(f"xpath={var_gpstaxi.txtNoteAdd}", var_gpstaxi.data['minitor']['hide_note'])

        self.page.context.once("dialog", lambda d: d.accept())#alert
        await self.page.click(f"xpath={var_gpstaxi.save_value}")
        try:
            self.page.context.once("dialog", lambda d: d.accept())      #lưu rồi thì phải đóng popup nhỏ Ẩn xe
        except:
            pass

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                              f"(//div[contains(@id,'HiddenVehicle')])//*[@role='grid']/tbody//*[text()='{var_gpstaxi.data['minitor']['hide_vehicle']}'][1]"
                                                              , var_gpstaxi.data['minitor']['hide_vehicle'], "_DanhSachXeDangAn_ThemXeAn.png")

        try:
            await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_add_new_x}", timeout=1000)
            print("Chưa đóng popup nhỏ ẩn xe")
        except:
            pass


    async def hidden_car_list_vehicle(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")

        await self.page.type(f"xpath={var_gpstaxi.acVehicleSearch}", var_gpstaxi.data['minitor']['hide_vehicle'])
        await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch_list1}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)
        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.k_select4_1_3, var_gpstaxi.data['minitor']['hide_vehicle'],
                                                                "__DanhSachXeDangAn_PhuongTien.png")


        await self.page.fill(f"xpath={var_gpstaxi.acVehicleSearch}", "")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)


    async def hidden_car_list_resson(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_resson_icon}")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_resson2}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.k_select4_1_10}")

        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_4}", timeout=2000)
        except:
            pass

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.HistoryHiddenVehicle1_4, "Xe sửa chữa,bảo dưỡng",
                                                                "__DanhSachXeDangAn_NguyenNhan.png")

        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_history_x}")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_resson_icon}")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_resson1}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)


    async def hidden_car_list_status(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_status_icon}")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_status_minitor}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.k_select4_1_4}", timeout=3000)
        except:
            pass

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.k_select4_1_4, "Ẩn trên giám sát", "_DanhSachXeDangAn_TrangThai.png")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_status_icon}")
        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_status_all}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)


    async def hidden_car_list_permission(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")


        checkbox = self.page.locator(var_gpstaxi.chkStopTransfer)
        if not await checkbox.is_checked():
            await checkbox.click()

        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)

        await module_other_gpstaxi.write_result_text_text_content_other(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.k_select4_1_5, "Truyền", "_DanhSachXeDangAn_CheckboxDungTruyen.png")

        await checkbox.click()
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)


    async def hidden_car_list_fee(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")


        checkbox = self.page.locator(var_gpstaxi.chkStopTransfer)
        if not await checkbox.is_checked():
            await checkbox.click()
            await asyncio.sleep(1)
            await checkbox.click()
            await asyncio.sleep(1)
        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Danh sách xe đang ẩn",
                                                                var_gpstaxi.chkStopTransfer, "_DanhSachXeDangAn_TatThongBaoXeDenHanThuPhi.png")


    async def hidden_car_lis_check_info(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")

        logging.info("Giám sát - Danh sách xe đang ẩn")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            stt = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_1}").text_content()
            number = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_2}").text_content()
            liscens_plate = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_3}").text_content()
            status = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_4}").text_content()
            permission = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_5}").text_content()
            permission_day = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_6}").text_content()
            fee = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_7}").text_content()
            person = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_8}").text_content()
            day_action = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_9}").text_content()

            logging.info(f"STT: {stt}\nSố xe: {number}\nBiển số: {liscens_plate}\n"
                         f"Trạng thái: {status}\nTruyền BCA: {permission}\nNgày truyền: {permission_day}"
                         f"Hạn phí: {fee}\nNgười thực hiện: {person}\nNgày thực hiện: {day_action}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                                         f"STT: {stt}\nSố xe: {number}\nBiển số: {liscens_plate}\n"
                                         f"Trạng thái: {status}\nTruyền BCA: {permission}\nNgày truyền: {permission_day}"
                                         f"Hạn phí: {fee}\nNgười thực hiện: {person}\nNgày thực hiện: {day_action}")

            if (stt == "1") and (number != "") and (liscens_plate != "") and (status != "") and\
                (permission != "") and (person != "") and (day_action != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_DanhSachXeDangAn_CheckThongTin.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_DanhSachXeDangAn_CheckThongTin.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_DanhSachXeDangAn_CheckThongTin.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")


    async def hidden_car_lis_history(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.k_select4_1_10}")

        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_4}", timeout=3000)
        except:
            pass

        logging.info("Giám sát - Danh sách xe đang ẩn")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            stt = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_1}").text_content()
            liscens_plate = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_2}").text_content()
            status = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_3}").text_content()
            resson = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_4}").text_content()
            note = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_5}").text_content()
            person = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_6}").text_content()
            day_action = await self.page.locator(f"xpath={var_gpstaxi.HistoryHiddenVehicle1_7}").text_content()

            logging.info(f"STT: {stt}\nBiển số: {liscens_plate}\nTrạng thái: {status}\nNguyên nhân: {resson}"
                         f"\nGhi chú: {note}\nNgười thực hiện: {person}\nNgày thực hiện: {day_action}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"STT: {stt}\nBiển số: {liscens_plate}\nTrạng thái: {status}\n"
                                                                                f"Nguyên nhân: {resson}\nGhi chú: {note}\nNgười thực hiện: {person}"
                                                                                f"Ngày thực hiện: {day_action}")

            if (stt == "1") and (liscens_plate != "") and (status != "") and (resson != "") and\
                (note != "") and (person != "") and (day_action != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_DanhSachXeDangAn_LichSu_CheckThongTin.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_DanhSachXeDangAn_LichSu_CheckThongTin.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_DanhSachXeDangAn_LichSu_CheckThongTin.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")

        await self.page.click(f"xpath={var_gpstaxi.hidden_car_list_history_x}")


    async def hidden_car_lis_cancel(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch}",  timeout=500)
        except:
            await IconPage.hidden_car_list_add_new(self, "", "", "")


        await self.page.type(f"xpath={var_gpstaxi.acVehicleSearch}", var_gpstaxi.data['minitor']['hide_vehicle'])
        await self.page.click(f"xpath={var_gpstaxi.acVehicleSearch_list1}")
        await self.page.click(f"xpath={var_gpstaxi.search_value}")
        await asyncio.sleep(1)


        try:
            vehicle = await self.page.locator(f"xpath={var_gpstaxi.k_select4_1_3}").inner_text(timeout=1500)
            print(vehicle)
            if vehicle == var_gpstaxi.data['minitor']['hide_vehicle']:
                print("chuẩn bị bỏ ẩn")

                locator = self.page.locator(f"xpath={var_gpstaxi.k_select4_1_11_icon}")
                await locator.scroll_into_view_if_needed()
                n = 1
                while (n < 5):
                    n = n + 1
                    try:
                        await locator.click(timeout=1500)
                        await asyncio.sleep(0.3)
                    except:
                        pass

                print("đã click")

                try:
                    await self.page.click(f"xpath={var_gpstaxi.no_permisson}", timeout=2000)
                except:
                    pass
                self.page.context.once("dialog", lambda d: d.accept())
                await module_other_gpstaxi.write_result_not_displayed(self.page, code, event, result,"Giám sát - Danh sách xe đang ẩn",
                                                                        f"(//div[contains(@id,'HiddenVehicle')])//*[@role='grid']/tbody//*[text()='{var_gpstaxi.data['minitor']['hide_vehicle']}'][1]"
                                                                      ,"_DanhSachXeDangAn_LoaiBo.png")
        except Exception as e:
            logging.error(f"Không tìm thấy phương tiện thêm mới: {e}")
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}_DanhSachXeDangAn_LoaiBo.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_DanhSachXeDangAn_LoaiBo")





    async def Search(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])

        await module_other_gpstaxi.write_result_text_content_handle_title(self.page, code, event, result, "Giám sát - Search",
                                                                    var_gpstaxi.search_title, "Google Maps", "_GiamSat_Search.png")


    async def Monitor_multiple_vehicles(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.Monitor_multiple_vehicles, var_gpstaxi.Current_Status,
                                                                    "Hiện trạng", "_GiamSat_GiamSatNhieuXe.png")



    async def Measure_distance(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])
        await self.page.click(f"xpath={var_gpstaxi.Measure_distance}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.distanceWindow_wnd_title}")

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Đo khoảng cách",
                                                                var_gpstaxi.distanceWindow_wnd_title, "Đo khoảng cách",
                                                                "_GiamSat_DoKhoangCach.png")


    async def Measure_distance_select_2_point(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.radDistanceType}",  timeout=500)
        except:
            await IconPage.Measure_distance(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="left", position={"x": 470, "y": 450})
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="left", position={"x": 830, "y": 450})
        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Đo khoảng cách",
                                                                var_gpstaxi.marker_icon2, "_DoKhoangCach_Do2Diem.png")


    async def Measure_distance_check(self, code, event, result, button, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.radDistanceType}",  timeout=250)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.marker_icon2}", timeout=250)
        except:
            await IconPage.Measure_distance_select_2_point(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.unitsDropdown}")
        await self.page.click(f"xpath={button}")
        await asyncio.sleep(0.5)

        await module_other_gpstaxi.write_result_text_text_content_other(self.page, code, event, result, "Giám sát - Đo khoảng cách",
                                                                var_gpstaxi.distanceMajor, "0.00", name_image)


    async def Measure_distance_reset(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.radDistanceType}",  timeout=250)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.marker_icon2}", timeout=250)
        except:
            await IconPage.Measure_distance_select_2_point(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.Measure_distance_reset}")
        await asyncio.sleep(0.5)
        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Đo khoảng cách",
                                                                var_gpstaxi.distanceMajor, "0.00", "_DoKhoangCach_ThietLapLai.png")



    async def Guide(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])

        await module_other_gpstaxi.write_result_text_content_handle_title(self.page, code, event, result, "Giám sát - Dẫn đường",
                                                                    var_gpstaxi.Guide, "Google Maps", "_GiamSat_DanDuong.png")


    async def Check_fee(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhanh_tk'], var_gpstaxi.data['login']['binhanh_mk'])
        await self.page.click(f"xpath={var_gpstaxi.Check_fee}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.priceCheckWindow_wnd_title}")

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Tra cước",
                                                                var_gpstaxi.priceCheckWindow_wnd_title, "Tra cước", "_GiamSat_TraCuoc.png")


    async def Check_fee_payment(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.txtEnterKmNumber}",  timeout=500)
        except:
            await IconPage.Check_fee(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.Check_fee_type_vehicle}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.ddlPriceCheckVehicleType_listbox_spark_ls}")

        await self.page.click(f"xpath={var_gpstaxi.Check_fee_route}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.Check_fee_route_htv_bg}")

        await self.page.fill(f"xpath={var_gpstaxi.txtEnterKmNumber}", "50")

        await self.page.click(f"xpath={var_gpstaxi.Check_fee_payment}")
        await asyncio.sleep(1)

        logging.info("Giám sát - Danh sách xe đang ẩn")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            money1 = await self.page.locator(f"xpath={var_gpstaxi.txtMoneyOfOneWay}").input_value()
            money2 = await self.page.locator(f"xpath={var_gpstaxi.txtMoneyOfTwoWays}").input_value()
            note = await self.page.locator(f"xpath={var_gpstaxi.lblFormula}").text_content()

            logging.info(f"Tiền chiều đi: {money1}\nTiền 2 chiều: {money2}\n{note}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tiền chiều đi: {money1}\nTiền 2 chiều: {money2}\n{note}")

            if (money1 != "") and (money1 != "") and (note != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_TraCuoc_TinhTien.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_TraCuoc_TinhTien.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_TraCuoc_TinhTien.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")







    async def Make_an_appointment(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhanh_tk'], var_gpstaxi.data['login']['binhanh_mk'])
        await self.page.click(f"xpath={var_gpstaxi.Make_an_appointment}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.divEditAppointment_wnd_title}")

        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Đặt lịch hẹn",
                                                                var_gpstaxi.divEditAppointment_wnd_title, "Thêm mới thông tin lịch hẹn", "_GiamSat_DatLichHen.png")


    async def Make_an_appointment_fill(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.CustomerName}",  timeout=500)
        except:
            await IconPage.Make_an_appointment(self, "", "", "")

        await self.page.fill(f"xpath={var_gpstaxi.CustomerName}", "Trần Quang Trường")
        await self.page.fill(f"xpath={var_gpstaxi.PhoneNumber}", "0359667655")
        await self.page.fill(f"xpath={var_gpstaxi.Address}", "Số 01 TT3, Khu đô thị Tây Nam Linh Đàm, Hoàng Mai, Hà Nội, Việt Nam")
        await self.page.fill(f"xpath={var_gpstaxi.TimeToComeStr}", "08:00")
        await self.page.fill(f"xpath={var_gpstaxi.alert_before}", "20")
        await self.page.fill(f"xpath={var_gpstaxi.StartDate}", "")

        await self.page.click(f"xpath={var_gpstaxi.IsMultiDays}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.EndDate}")
        await self.page.click(f"xpath={var_gpstaxi.Mon}")
        await self.page.click(f"xpath={var_gpstaxi.Tue}")
        await self.page.click(f"xpath={var_gpstaxi.Wed}")
        await self.page.click(f"xpath={var_gpstaxi.Fri}")
        await self.page.click(f"xpath={var_gpstaxi.Sat}")
        await self.page.click(f"xpath={var_gpstaxi.Sun}")
        await self.page.click(f"xpath={var_gpstaxi.AllDay}")

        await self.page.fill(f"xpath={var_gpstaxi.Route}", "Trường test đặt lịch hẹn")
        await self.page.fill(f"xpath={var_gpstaxi.RequestVehicles}", "Accent, 2")
        await self.page.fill(f"xpath={var_gpstaxi.PrivateCodes}", "1012")

        await self.page.click(f"xpath={var_gpstaxi.PaymentTypeId_listbox}")
        # await asyncio.sleep(1)
        # await self.page.wait_for_selector(f"xpath={var_gpstaxi.PaymentTypeId_listbox1}")

        await self.page.click(f"xpath={var_gpstaxi.CustomerTypeId_listbox}")
        # await asyncio.sleep(1)
        # await self.page.wait_for_selector(f"xpath={var_gpstaxi.CustomerTypeId_listbox1}")

        await self.page.click(f"xpath={var_gpstaxi.DepositMoney1}")
        await self.page.fill(f"xpath={var_gpstaxi.DepositMoney}", "2000000")

        await self.page.click(f"xpath={var_gpstaxi.TotalMoney1}")
        await self.page.fill(f"xpath={var_gpstaxi.TotalMoney}", "2500000")

        await self.page.click(f"xpath={var_gpstaxi.TotalFee1}")
        await self.page.fill(f"xpath={var_gpstaxi.TotalFee}", "300000")

        await self.page.fill(f"xpath={var_gpstaxi.Note}", "Trường test thêm mới lịch hẹn")

        logging.info("Giám sát - Đặt lịch hẹn")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        logging.info("Pass")
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")


    async def Make_an_appointment_checkbutton(self, code, event, result, button, desire, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.CustomerName}",  timeout=500)
        except:
            await IconPage.Make_an_appointment(self, "", "", "")


        await module_other_gpstaxi.write_result_text_text_content(self.page, code, event, result, "Giám sát - Đặt lịch hẹn",
                                                                button, desire, name_image)


    async def Make_an_appointment_exit(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.CustomerName}",  timeout=500)
        except:
            await IconPage.Make_an_appointment(self, "", "", "")

        await module_other_gpstaxi.write_result_close(self.page, code, event, result, "Giám sát - Đặt lịch hẹn",
                                                                    var_gpstaxi.btnAbort, "_DatLichHen_Thoat.png")




    async def Appointment_list(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhanh_tk'], var_gpstaxi.data['login']['binhanh_mk'])

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Danh sách cuộc hẹn",
                                                                var_gpstaxi.Appointment_list, var_gpstaxi.panel_title, "Thông tin lịch hẹn", "_GiamSat_DanhSachLichHen.png")




    async def Lobby_area_warning(self, code, event, result):
        await self.login_page.goto("Mã XN", "369", "Nội Bài [369]")

        await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Cảnh báo vùng sảnh",
                                                                var_gpstaxi.ZoneWarningWindow_wnd_title, "Thông tin chi tiết cảnh báo Vùng/Sảnh/Xe ngoại thành",
                                                                "_GiamSat_CanhBaoVungSanh.png")


    async def Lobby_area_warning_area(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_area}",  timeout=500)
        except:
            await IconPage.Lobby_area_warning(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_area}")

        await asyncio.sleep(3.5)
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.ZoneWarningGrid1_1}")

        logging.info("Giám sát - Cảnh báo vùng sảnh")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            filed1 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_1}").text_content()
            filed2 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_2}").text_content()
            filed3 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_3}").text_content()

            logging.info(f"Tên vùng: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tên vùng: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")

            if (filed1 != "") and (filed2 != "") and (filed3 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_CanhBaoVungSanh_Vung.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")


    async def Lobby_area_warning_lobby(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_lobby}",  timeout=500)
        except:
            await IconPage.Lobby_area_warning(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_lobby}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.Lobby_area_warning_nodata}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Cảnh báo vùng sảnh",
                                                                var_gpstaxi.Lobby_area_warning_nodata, "Không có dữ liệu", "_CanhBaoVungSanh_Sanh.png")


        # await self.page.wait_for_selector(f"xpath={var_gpstaxi.ZoneWarningGrid1_1}")
        #
        # logging.info("Giám sát - Cảnh báo vùng sảnh")
        # logging.info(f"Mã - {code}")
        # logging.info(f"Tên sự kiện - {event}")
        # logging.info(f"Kết quả - {result}")
        # try:
        #     filed1 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_1}").text_content()
        #     filed2 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_2}").text_content()
        #     filed3 = await self.page.locator(f"xpath={var_gpstaxi.ZoneWarningGrid1_3}").text_content()
        #
        #     logging.info(f"Tên vùng: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")
        #
        #     module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tên vùng: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")
        #
        #     if (filed1 != "") and (filed2 != "") and (filed3 != ""):
        #         logging.info("Pass")
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        #     else:
        #         logging.info("Fail")
        #         await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
        #         module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_CanhBaoVungSanh_Vung.png")
        # except Exception as e:
        #     logging.info(f"Fail - {e}")
        #     await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
        #     module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")


    async def Lobby_area_warning_suburb(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_suburb}",  timeout=500)
        except:
            await IconPage.Lobby_area_warning(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_suburb}")

        filed1 = await self.page.locator(f"xpath={var_gpstaxi.ExtramuralWarningGrid1_1}").text_content()
        print(f"filed1: {filed1}")

        logging.info("Giám sát - Cảnh báo vùng sảnh")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            filed1 = await self.page.locator(f"xpath={var_gpstaxi.ExtramuralWarningGrid1_1}").text_content()
            filed2 = await self.page.locator(f"xpath={var_gpstaxi.ExtramuralWarningGrid1_2}").text_content()
            filed3 = await self.page.locator(f"xpath={var_gpstaxi.ExtramuralWarningGrid1_3}").text_content()
            filed3 = filed3[0:30]

            logging.info(f"Tên: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tên: {filed1}\nSố xe: {filed2}\nChi tiết: {filed3}")

            if (filed1 != "") and (filed2 != "") and (filed3 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_CanhBaoVungSanh_Vung.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_CanhBaoVungSanh_Vung.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")


    async def Lobby_area_warning_update(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.btnPriceCheckSave}",  timeout=500)
        except:
            await IconPage.Lobby_area_warning(self, "", "", "")

        await module_other_gpstaxi.write_result_status_code(self.page, code, event, result, "Giám sát - Cảnh báo vùng sảnh",
                                                                var_gpstaxi.btnPriceCheckSave, "/ZoneWarning/LoadListVehilceInOperatingArea",
                                                            "_CanhBaoVungSanh_CapNhat.png")


    async def Lobby_area_warning_exit(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.Lobby_area_warning_lobby}")
            await self.page.click(f"xpath={var_gpstaxi.btnPriceCheckSave}",  timeout=500)
        except:
            await IconPage.Lobby_area_warning(self, "", "", "")

        await module_other_gpstaxi.write_result_close(self.page, code, event, result, "Giám sát - Cảnh báo vùng sảnh",
                                                                    var_gpstaxi.btnPriceCheckCancel, "_CanhBaoVungSanh_Thoat.png")



class ListVehicle:

    def __init__(self, page):
        self.page = page  # Page Playwright async
        self.login_page = Login(page)  # Dùng Login async


    async def ListVehicle_combobox(self, code, event, result, path_module, button, path_check, name_image):
        if name_image == "_GiamSat_NhomDoi.png":
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                                var_gpstaxi.data['login']['batest424_mk'])

        try:
            await self.page.click(f"xpath={button}", timeout=1500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                                var_gpstaxi.data['login']['batest424_mk'])
            await self.page.click(f"xpath={button}")

        await self.page.wait_for_selector(f"xpath={path_check}")
        await module_other_gpstaxi.write_result_text_text_content_other(self.page, code, event, result, path_module,
                                                          path_check, "", name_image)


    async def Search_vehicle(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                            var_gpstaxi.data['login']['binhthuong_mk'])


        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox}")
        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox_vehicle}")

        vehicle = await self.page.locator(f"xpath={var_gpstaxi.tblVehicleList3_2}").text_content()
        await self.page.type(f"xpath={var_gpstaxi.Online_Vehicles_input}", vehicle)
        await self.page.click(f"xpath={var_gpstaxi.Online_Vehicles_listbox1}")

        await self.page.click(f"xpath={var_gpstaxi.btnVehicleSearch}")
        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Tìm kiếm xe",
                                                                var_gpstaxi.VehicleStatus, vehicle, "_GiamSat_TimKiemXe.png")

        await self.page.click(f"xpath={var_gpstaxi.hide_detail_vehicle}")


    async def Search_address(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.Layers}", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox}")
        await module_other_gpstaxi.write_result_text_content_handle_title(self.page, code, event, result, "Giám sát - Tìm địa chỉ",
                                                                    var_gpstaxi.ddlSearchProperty_listbox_address, "Google Maps", "_GiamSat_TimDiaChi.png")


    async def Search_landmark(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.Layers}", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox}")
        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox_landmark}")

        await self.page.type(f"xpath={var_gpstaxi.cbLandMark_input}", var_gpstaxi.data['minitor']['landmark'])
        await self.page.click(f"xpath={var_gpstaxi.cbLandMark_listbox1}")
        await self.page.click(f"xpath={var_gpstaxi.btnVehicleSearch}")


        await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Search_landmark}")
        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Tìm tên điểm", var_gpstaxi.check_Search_landmark,
                                                                   var_gpstaxi.data['minitor']['landmark'], "_GiamSat_TimTenDiem.png")

        await self.login_page.delete_notication()


    async def Search_coordinates(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.Layers}", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox}")
        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox_coordinates}")

        await self.page.type(f"xpath={var_gpstaxi.txtPointSearch}", var_gpstaxi.data['minitor']['coordinates'])
        await self.page.click(f"xpath={var_gpstaxi.btnVehicleSearch}")

        await asyncio.sleep(1.5)
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_Search_coordinates}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Tìm tên điểm", var_gpstaxi.check_Search_coordinates,
                                                                   "Vĩ độ : 20.981636 , Kinh độ : 105.829496", "_GiamSat_TimToaDo.png")


    async def Status(self, code, event, result, type, status, name_image):
        #Login bt permission
        if type == "have_group":
            try:
                await self.page.wait_for_selector(f"xpath=//*[text()='Cty CP Điện Tử TH Viễn Thông EG [9040]']", timeout=500)
            except:
                await self.login_page.goto("Mã XN", "9040", "Cty CP Điện Tử TH Viễn Thông EG [9040]")

        if type == "no_group":
            try:
                await self.page.wait_for_selector(f"xpath=//*[text()='CÔNG TY TNHH  MẬN VŨ [450]']", timeout=500)
            except:
                await self.login_page.goto("Mã XN", "450", "CÔNG TY TNHH  MẬN VŨ [450]")


        await self.page.click(f"xpath={var_gpstaxi.Online_VehicleStatus_listbox}")
        await asyncio.sleep(1)

        try:
            await self.page.click(f"xpath=//*[@id='Online_VehicleStatus_listbox']//*[text()='{status}']", timeout=2000)
        except:
            await self.page.click(f"xpath={var_gpstaxi.Online_VehicleStatus_listbox}")
            await asyncio.sleep(1)
            await self.page.click(f"xpath=//*[@id='Online_VehicleStatus_listbox']//*[text()='{status}']")
        await asyncio.sleep(1.5)

        summary_vehicle_select = await self.page.locator(f"xpath={var_gpstaxi.spCurrent}").inner_text()
        summary_vehicle = await self.page.locator(f"xpath={var_gpstaxi.spTotal}").inner_text()
        print(f"Tổng xe chọn: {summary_vehicle_select}")
        print(f"Tổng xe: {summary_vehicle}")

        n = 1
        while (n < 100):
            n = n + 1
            path_vehilce = f"//*[@id='tblVehicleList']/tbody/tr[{str(n)}]/td[2]"
            try:
                name_vehicle = await self.page.locator(f"xpath={path_vehilce}").inner_text(timeout=300)
                print(f"xe: {n-2}, {name_vehicle}")
            except:
                print("--------------------------------------")
                print(f"Tổng xe chọn: {summary_vehicle_select}")
                print(f"Tổng xe: {summary_vehicle}")
                print(f"Trạng thái: {status}, có {n-2} xe")
                var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 3, 2, n-2)
                break




        logging.info("Giám sát - Check trạng thái")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        vehicle_list = int(var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 3, 2))

        logging.info(f"Tổng xe chọn: {summary_vehicle_select}\n"
                     f"Danh sách xe: {vehicle_list}\n"
                     f"Tổng xe     : {summary_vehicle}")

        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tổng xe chọn: {summary_vehicle_select}\n"
                                                                            f"Danh sách xe: {vehicle_list}\n"
                                                                            f"Tổng xe     : {summary_vehicle}")
        if status == "Tất cả":
            if int(summary_vehicle_select) == int(vehicle_list) == int(summary_vehicle):
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")

        else:
            if int(summary_vehicle_select) == int(vehicle_list):
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")


    async def Icon_refresh(self, code, event, result):
        await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await module_other_gpstaxi.write_result_status_code(self.page, code, event, result, "Giám sát - Danh sách xe - Icon làm mới",
                                                                var_gpstaxi.icon_refresh_new_data, "/Online/RequestSyn?",  "_GiamSat_DanhSachXe_IconLamMoi.png")


    async def System_status(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")


        await self.page.click(f"xpath={var_gpstaxi.btnSystemStatus}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.windowCurrentSystem_wnd_title}", timeout=5000)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Icon hiện trạng hệ thống",
                                                                   var_gpstaxi.windowCurrentSystem_wnd_title, "Hiện trạng hệ thống", "_GiamSat_HienTrangHeThong.png")


    async def System_status_check(self, code, event, result, status, name_id, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}",  timeout=500)
        except:
            await ListVehicle.System_status(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}")

        await asyncio.sleep(1)
        await self.page.click(f"xpath=//*[@id='currentSystem_listbox']//*[text()='"+status+"']")
        await asyncio.sleep(2.5)

        logging.info("Giám sát - Icon")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            field1 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[1]").inner_text(timeout=7000)
            field2 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[2]").inner_text()
            field3 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[3]").inner_text()
            field4 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[4]").inner_text()
            field5 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[5]").inner_text()
            field6 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[6]").inner_text()
            field7 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[7]").inner_text()
            field8 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[8]").inner_text()
            field9 = await self.page.locator(f"xpath=//*[@id='{name_id}']/table/tbody[1]/tr[1]/td[9]").inner_text()

            logging.info(f"STT: {field1}\n"
                         f"Số xe: {field2}\n"
                         f"Biển số: {field3}\n"
                         f"IMEI: {field4}\n"
                         f"SIM: {field5}\n"
                         f"Vgps/cơ(Dừng đỗ (phút)): {field6}\n"
                         f"Thời gian: {field7}\n"
                         f"Km trong ngày: {field8}\n"
                         f"Khu vực: {field9}\n")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                         f"STT: {field1}\n"
                         f"Số xe: {field2}\n"
                         f"Biển số: {field3}\n"
                         f"IMEI: {field4}\n"
                         f"SIM: {field5}\n"
                         f"Vgps/cơ: {field6}\n"
                         f"Thời gian: {field7}\n"
                         f"Km trong ngày: {field8}\n"
                         f"Khu vực: {field9}\n")


            if (field1 != "") and (field2 != "") and (field3 != "") and (field6 != "") \
                    and (field7 != "") and (field8 != "") and (field9 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")
        except Exception as e:
            try:
                nodata = await self.page.locator(f"xpath=//*[@id='{name_id}']//*[text()='Không có dữ liệu']").inner_text()
                logging.info(nodata)
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, nodata)
            except:
                logging.info(f"Fail - {e}")
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")


    async def System_status_list_vehicle_active(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}",  timeout=500)
        except:
            await ListVehicle.System_status(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}")

        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.System_status_list_vehicle_active}")
        await asyncio.sleep(2.5)

        logging.info("Giám sát - Icon")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            field1 = await self.page.locator(f"xpath={var_gpstaxi.ActiveList1_1}").inner_text()
            field2 = await self.page.locator(f"xpath={var_gpstaxi.ActiveList1_2}").inner_text()
            field3 = await self.page.locator(f"xpath={var_gpstaxi.ActiveList1_3}").inner_text()
            field4 = await self.page.locator(f"xpath={var_gpstaxi.ActiveList1_4}").inner_text()

            logging.info(f"STT: {field1}\nSố xe: {field2}\n"
                         f"Số KM: {field3}\nThời gian hoạt động: {field4}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                                           f"STT: {field1}\nSố xe: {field2}\n"
                                           f"Số KM: {field3}\nThời gian hoạt động: {field4}")


            if (field1 != "") and (field2 != "") and (field3 != "") and (field4 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_HienTrangHeThong_DanhSachXeHoatDong.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_HienTrangHeThong_DanhSachXeHoatDong.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_HienTrangHeThong_DanhSachXeHoatDong.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_HienTrangHeThong_DanhSachXeHoatDong.png")


    async def System_status_excel(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}",  timeout=500)
        except:
            await ListVehicle.System_status(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}")

        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.System_status_have_guests}")
        await asyncio.sleep(2.5)

        await module_other_gpstaxi.write_result_web_excel(self.page, code, event, result, "Hiện trạng hệ thống - Xuất excel",
                                                      var_gpstaxi.btnExportExcel, "//*[@id='contentCurrentSystem']//table/thead//th",
                                                       "//*[@id='contentCurrentSystem']//table/tbody/tr[1]/td", 5, 9)

        try:
            await self.page.click(f"xpath={var_gpstaxi.windowCurrentSystem_wnd_title_x}")
            await asyncio.sleep(1)
        except:
            print("Chưa đóng popup")


    async def Car_symbol_meaning(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")


        await self.page.click(f"xpath={var_gpstaxi.btnHelp}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.helpWindow_wnd_title}", timeout=5000)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Icon ý nghĩa biểu tượng xe",
                                                                   var_gpstaxi.helpWindow_wnd_title, "Ý nghĩa màu sắc và biểu tượng của xe", "_GiamSat_YNghiaBieuTuongXe.png")

        try:
            await self.page.click(f"xpath={var_gpstaxi.helpWindow_wnd_title_x}")
            await asyncio.sleep(1)
        except:
            print("Chưa đóng popup")


    async def Share_vehicle(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")


        await self.page.click(f"xpath={var_gpstaxi.btnShare}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.shareVehicleWindow_wnd_title}", timeout=5000)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Icon Chia sẻ phương tiện",
                                                                   var_gpstaxi.shareVehicleWindow_wnd_title, "Chia sẻ phương tiện", "_GiamSat_ChiaSePhuongTien.png")


    async def Share_vehicle_fill(self, type):
        try:
            await self.page.click(f"xpath={var_gpstaxi.FromTimeShare}",  timeout=500)
        except:
            await ListVehicle.Share_vehicle(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.ddlShareFunction_listbox}")
        await asyncio.sleep(1.2)

        if type == "minitor":
            await self.page.click(f"xpath={var_gpstaxi.ddlShareFunction_listbox_minitor}")
        if type == "route":
            await self.page.click(f"xpath={var_gpstaxi.ddlShareFunction_listbox_route}")
            await asyncio.sleep(1)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.ExpiredDateShare}")#Thời gian hết hạn link chia sẻ
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.ExpiredTimeShare}")#Thời gian hết hạn link chia sẻ


        await self.page.click(f"xpath={var_gpstaxi.ms_parent1}")#Nhóm phương tiện
        await asyncio.sleep(1)
        checkbox = self.page.locator(var_gpstaxi.ms_parent1_li1)
        if not await checkbox.is_checked():
            await checkbox.click()
            await asyncio.sleep(1)

        await self.page.click(f"xpath={var_gpstaxi.ms_parent2}")#Phương tiện
        await asyncio.sleep(1)
        checkbox = self.page.locator(var_gpstaxi.ms_parent2_li2)
        if not await checkbox.is_checked():
            await checkbox.click()
            await asyncio.sleep(1)


        await self.page.click(f"xpath={var_gpstaxi.FromTimeShare}")
        await self.page.click(f"xpath={var_gpstaxi.FromDateShare}")
        await self.page.click(f"xpath={var_gpstaxi.ToTimeShare}")
        await self.page.click(f"xpath={var_gpstaxi.ToDateShare}")

        checkbox = self.page.locator(var_gpstaxi.cbxShowLandmark)
        if not await checkbox.is_checked():
            await checkbox.click()

        checkbox = self.page.locator(var_gpstaxi.cbxAll)
        if not await checkbox.is_checked():
            await checkbox.click()

        self.page.context.once("dialog", lambda d: d.accept())#alert
        await self.page.click(f"xpath={var_gpstaxi.create_and_share}")


    async def Share_vehicle_fill_and_coppy(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.FromTimeShare}",  timeout=500)
        except:
            await ListVehicle.Share_vehicle(self, "", "", "")

        await ListVehicle.Share_vehicle_fill(self, "minitor")

        await self.page.click(f"xpath={var_gpstaxi.coppy}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Icon Chia sẻ phương tiện",
                                                                   var_gpstaxi.coppy_success, "Sao chép thành công", "_ChiaSePhuongTien_SaoChep.png")

        await module_other_gpstaxi.write_result_value_other(self.page, code, event, result, "Giám sát - Icon Chia sẻ phương tiện",
                                                                   var_gpstaxi.txtLinkShare, "", "_ChiaSePhuongTien_LinkChiaSe.png")


    async def Share_vehicle_minitor(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.FromTimeShare}",  timeout=500)
        except:
            await ListVehicle.Share_vehicle(self, "", "", "")

        await ListVehicle.Share_vehicle_fill(self, "minitor")

        async with self.page.context.expect_page() as new_page_info:
            await self.page.click(f"xpath={var_gpstaxi.btnPreview}")

        # LẤY TAB MỚI (phải có await)
        new_page = await new_page_info.value

        # Đợi tab mới load
        await new_page.wait_for_load_state("load", timeout=15000)



        # ---------- BẮT ĐẦU XỬ LÝ ----------
        logging.info("Giám sát - Icon Chia sẻ phương tiện")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        try:
            locator = new_page.locator(f"xpath={var_gpstaxi.remaintime}").first
            filed1 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_vehicle}").first
            filed2 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_km}").first
            filed3 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_time}").first
            filed4 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_vehicle2}").first
            filed5 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_speed}").first
            filed6 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_address}").first
            filed7 = await locator.inner_text()

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{filed1}\nPhương tiện: {filed2}\nKm/h: {filed3}\nThời gian: {filed4}\n"
                                                                                f"Biển kiểm soát: {filed5}\nVận tốc GPS: {filed6}\nĐịa chỉ: {filed7}")

            logging.info(f"{filed1}\nPhương tiện: {filed2}\nKm/h: {filed3}\nThời gian; {filed4}\n"
                         f"Biển kiểm soát: {filed5}\nVận tốc GPS: {filed6}\nĐịa chỉ: {filed7}")

            if all([filed1, filed2, filed3, filed4, filed5, filed6, filed7]):    #Tự động xử lý trường hợp "", None, 0, hoặc False
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                await new_page.screenshot(path=f"{imagepath}{code}_ChiaSePhuongTien_GiamSat.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_ChiaSePhuongTien_GiamSat.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await new_page.screenshot(path=f"{imagepath}{code}_ChiaSePhuongTien_GiamSat.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_ChiaSePhuongTien_GiamSat.png")

        await new_page.close()


    async def Share_vehicle_route(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.FromTimeShare}",  timeout=500)
        except:
            await ListVehicle.Share_vehicle(self, "", "", "")

        await ListVehicle.Share_vehicle_fill(self, "route")


        async with self.page.context.expect_page() as new_page_info:
            await self.page.click(f"xpath={var_gpstaxi.btnPreview}")

        # LẤY TAB MỚI (phải có await)
        new_page = await new_page_info.value

        # Đợi tab mới load
        await new_page.wait_for_load_state("load", timeout=15000)



        # ---------- BẮT ĐẦU XỬ LÝ ----------
        logging.info("Giám sát - Icon Chia sẻ phương tiện")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        try:
            locator = new_page.locator(f"xpath={var_gpstaxi.route_remaintime}").first
            filed1 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_route_vehicle}").first
            filed2 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_route_time}").first
            filed3 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_route_address1}").first
            filed4 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_route_address2}").first
            filed5 = await locator.inner_text()

            locator = new_page.locator(f"xpath={var_gpstaxi.Share_vehicle_minitor_summary}").first
            filed6 = await locator.inner_text()

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{filed1}\n{filed2}\nThời gian lộ trình: {filed3}\nĐịa điểm bắt đầu: {filed4}\n"
                                                                                f"Địa điểm kết thúc: {filed5}\nTổng quãng đường: {filed6}")

            logging.info(f"{filed1}\n{filed2}\nThời gian lộ trình: {filed3}\nĐịa điểm bắt đầu: {filed4}\n"
                         f"Địa điểm kết thúc: {filed5}\nTổng quãng đường: {filed6}")

            if all([filed1, filed2, filed3, filed4, filed5, filed6]):    #Tự động xử lý trường hợp "", None, 0, hoặc False
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                await new_page.screenshot(path=f"{imagepath}{code}_ChiaSePhuongTien_LoTrinh.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_ChiaSePhuongTien_LoTrinh.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await new_page.screenshot(path=f"{imagepath}{code}_ChiaSePhuongTien_LoTrinh.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_ChiaSePhuongTien_LoTrinh.png")

        await new_page.close()

        try:
            await self.page.click(f"xpath={var_gpstaxi.shareVehicleWindow_wnd_title_x}")
            await asyncio.sleep(1)
        except:
            print("Chưa đóng popup")


    async def get_vehicle_times(self, path_vehilce):
        # Bắt API InfoWindoGenerator
        async with self.page.expect_response("**/InfoWindoGenerator**") as resp_info:
            await self.page.click(f"xpath={path_vehilce}")

        await asyncio.sleep(3)
        resp = await resp_info.value

        # Lấy URL của API
        url = resp.url

        # Tách query string
        params = parse_qs(urlparse(url).query)

        # Lấy 2 giá trị bạn cần

        gps_time = params.get("gpsTime", [""])[0]
        # vehicle_time = params.get("vehicleTime", [""])[0]
        privateCode = params.get("privateCode", [""])[0]

        return gps_time, privateCode


    async def Check_online_vehicle(self, code, event, result):
        module_other_gpstaxi.clearData_luutamthoi_from(var_gpstaxi.path_luutamthoi, "Sheet2", "", "", "", 1, 5)

        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        n = 1
        while (n < 6):
            n = n + 1
            path_vehilce = f"(//table[contains(@id,'tblVehicleList')])/tbody/tr[{str(n)}]/td[2]"
            try:
                gps_time, privateCode = await self.get_vehicle_times(path_vehilce)
                print(f"Xe {n-1}, privateCode: {privateCode}")
                print(f"Xe {n-1}, gps_time   : {gps_time}")
                var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet2", n, 2, privateCode)
                var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet2", n, 3, gps_time)
            except:
                print(f"đã lấy xong api {n} xe.")
                break



        vehicle_privateCode1 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 2, 2)
        vehicle_privateCode2 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 3, 2)
        vehicle_privateCode3 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 4, 2)
        vehicle_privateCode4 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 5, 2)
        vehicle_privateCode5 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 6, 2)

        vehicle_time1 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 2, 3)
        vehicle_time2 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 3, 3)
        vehicle_time3 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 4, 3)
        vehicle_time4 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 5, 3)
        vehicle_time5 = module_other_gpstaxi.readData(var_gpstaxi.path_luutamthoi, "Sheet2", 6, 3)

        vehicle_times = [
            vehicle_time1,
            vehicle_time2,
            vehicle_time3,
            vehicle_time4,
            vehicle_time5
        ]

        current = datetime.now()
        threshold = current - timedelta(minutes=3)

        count = 0
        for vt in vehicle_times:
            if not vt:  # nếu None hoặc chuỗi rỗng → bỏ qua
                continue

            vt = vt.replace("  ", " ").strip()

            t = datetime.strptime(vt, "%H:%M %d/%m/%Y")
            if t < threshold:
                count += 1

        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        logging.info(f"Thời gian hiện tại: {current}\n"
                     f"Số xe 1: {vehicle_privateCode1}, gps_time: {vehicle_time1}\n"
                     f"Số xe 2: {vehicle_privateCode2}, gps_time: {vehicle_time2}\n"
                     f"Số xe 3: {vehicle_privateCode3}, gps_time: {vehicle_time3}\n"
                     f"Số xe 4: {vehicle_privateCode4}, gps_time: {vehicle_time4}\n"
                     f"Số xe 5: {vehicle_privateCode5}, gps_time: {vehicle_time5}")

        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                     f"Thời gian hiện tại: {current}\n"
                     f"Số xe 1: {vehicle_privateCode1}, gps_time: {vehicle_time1}\n"
                     f"Số xe 2: {vehicle_privateCode2}, gps_time: {vehicle_time2}\n"
                     f"Số xe 3: {vehicle_privateCode3}, gps_time: {vehicle_time3}\n"
                     f"Số xe 4: {vehicle_privateCode4}, gps_time: {vehicle_time4}\n"
                     f"Số xe 5: {vehicle_privateCode5}, gps_time: {vehicle_time5}")

        if count >= 3:
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_CheckApi5Xe.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_CheckApi5Xe")
        else:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")


    async def Check_countvehicle_web_api(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['taxihathanh_tk'],
                                            var_gpstaxi.data['login']['taxihathanh_mk'])


        async with self.page.expect_response("**/Common/AutoCompletePrivateCodeByUserWithHiddenVehicle") as resp_info:
            await self.page.reload()

        resp = await resp_info.value

        # Status code
        print("Status:", resp.status)

        # Lấy JSON trả về
        data = await resp.json()
        if not isinstance(data, list):
            raise AssertionError("API không trả về danh sách")

        total_false = sum(
            1 for item in data
            if isinstance(item, dict) and item.get("IsVehiclePlateChanged") is False
        )

        print("Tổng IsVehiclePlateChanged = false:", total_false)

        summary_vehicle = await self.page.locator(f"xpath={var_gpstaxi.spTotal}").inner_text()

        dcount = 0
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        logging.info(f"Tổng xe danh sách: {summary_vehicle}\n"
                     f"Tổng xe api      : {total_false}")

        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tổng xe danh sách: {summary_vehicle}\n"
                                                                            f"Tổng xe api      : {total_false}")

        if int(summary_vehicle) == int(total_false):
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_CheckSoLuongXe_Api_Web.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_CheckSoLuongXe_Api_Web")


    async def Get_data_check(self, code, event, result):
        module_other_gpstaxi.clearData_luutamthoi_from(var_gpstaxi.path_luutamthoi, "Sheet1", "", "", "", 4, 37)
        await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await self.page.click(f"xpath={var_gpstaxi.Online_VehicleStatus_listbox}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.Online_VehicleStatus_listbox_have_guets}")
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList2_2}")
        await asyncio.sleep(1.5)

        VehicleStatus = await self.page.locator(f"xpath={var_gpstaxi.VehicleStatus}").inner_text()
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 29, 2, VehicleStatus)#Vị trí

        address = await self.page.locator(f"xpath={var_gpstaxi.tab1_1}").inner_text()
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 4, 2, address)#Vị trí


        #Click vào xe
        await get_info_status(self.page, "Loại xe", 5)
        await get_info_status(self.page, "Ngày/Giờ", 6)
        await get_info_status(self.page, "Lái xe", 7)
        await get_info_status(self.page, "Lái xe1", 7)
        await get_info_status(self.page, "Lái xe2", 8)
        await get_info_status(self.page, "Điện thoại", 9)
        await get_info_status(self.page, "Vận tốc GPS/Cơ", 10)
        await get_info_status(self.page, "Gara", 11)
        await get_info_status(self.page, "Đã dừng", 37)
        await get_info_status(self.page, "Điều hòa", 12)
        await get_info_status(self.page, "Máy", 13)
        await get_info_status(self.page, "Trạng thái", 14)
        await get_info_status(self.page, "Nhóm đội", 15)
        await get_info_status(self.page, "Loại đồng hồ", 16)
        await get_info_status(self.page, "KM CK/Rỗng", 17)
        await get_info_status(self.page, "Tổng CK", 18)
        await get_info_status(self.page, "Tổng doanh thu", 19)
        await get_info_status(self.page, "Tiền CK hiện tại", 20)
        await get_info_status(self.page, "Thời gian chờ", 21)
        await get_info_status(self.page, "KM CK đang chạy", 22)
        await get_info_status(self.page, "KM CK/Rỗng trong ca", 30)
        await get_info_status(self.page, "Tổng CK trong ca", 31)
        await get_info_status(self.page, "Tổng doanh thu trong ca", 32)

        await self.page.click(f"xpath={var_gpstaxi.tabs_2}")
        await asyncio.sleep(1.5)
        await get_info_bgt(self.page, "Lái xe", 23)
        await get_info_bgt(self.page, "Giấy phép lái xe", 24)
        await get_info_bgt(self.page, "Quá tốc độ", 25)
        await get_info_bgt(self.page, "TG LX liên tục", 26)
        await get_info_bgt(self.page, "TG LX trong ngày", 27)
        await get_info_bgt(self.page, "Sở quản lý", 28)


        #API
        async with self.page.expect_response("**/InfoWindoGenerator**") as resp_info:
            await self.page.click(f"xpath={var_gpstaxi.tblVehicleList2_2}")

        await asyncio.sleep(2)
        resp = await resp_info.value
        url = resp.url
        params = parse_qs(urlparse(url).query)

        privateCode = params.get("privateCode", [""])[0]
        vehiclePlate = params.get("vehiclePlate", [""])[0]
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 29, 3, f"{privateCode}-{vehiclePlate}")

        vehicleTime = params.get("vehicleTime", [""])[0]
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 6, 3, vehicleTime)

        seat = params.get("seat", [""])[0]
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 5, 3, seat)

        velocityGPS = params.get("velocityGPS", [""])[0]
        var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 10, 3, velocityGPS)

        try:
            await self.page.click(f"xpath={var_gpstaxi.hide_detail_vehicle}")
            await asyncio.sleep(1)
        except:
            pass



        #Popup Hiện trạng
        await self.page.click(f"xpath={var_gpstaxi.btnSystemStatus}")
        await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.currentSystem_listbox_have_guests}")
        await asyncio.sleep(1.5)


        n = 0
        while (n < 11):
            n = n + 1
            Passenger_privateCode = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[2]"
            Passenger_vehicle_plate = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[3]"
            Passenger_imei = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[4]"
            Passenger_sim = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[5]"
            Passenger_velocityGPS = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[6]"
            Passenger_vehicleTime = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[7]"
            Passenger_km_in_day = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[8]"
            Passenger_address = f"//*[@id='Passenger']/table/tbody/tr[{str(n)}]/td[9]"

            try:
                Passenger_privateCode = await self.page.locator(f"xpath={Passenger_privateCode}").inner_text(timeout=200)
                Passenger_vehicle_plate = await self.page.locator(f"xpath={Passenger_vehicle_plate}").inner_text(timeout=200)
                Passenger_imei = await self.page.locator(f"xpath={Passenger_imei}").inner_text(timeout=200)
                Passenger_sim = await self.page.locator(f"xpath={Passenger_sim}").inner_text(timeout=200)
                Passenger_velocityGPS = await self.page.locator(f"xpath={Passenger_velocityGPS}").inner_text(timeout=200)
                Passenger_vehicleTime = await self.page.locator(f"xpath={Passenger_vehicleTime}").inner_text(timeout=200)
                Passenger_km_in_day = await self.page.locator(f"xpath={Passenger_km_in_day}").inner_text(timeout=200)
                Passenger_address = await self.page.locator(f"xpath={Passenger_address}").inner_text(timeout=200)

                print(f"Passenger_privateCode: {Passenger_privateCode}")
                print(f"privateCode: {privateCode}")
                if Passenger_privateCode == privateCode:
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 29, 4, f"{Passenger_privateCode}-{Passenger_vehicle_plate}")
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 34, 4, Passenger_imei)
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 35, 4, Passenger_sim)
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 10, 4, Passenger_velocityGPS)
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 6, 4, Passenger_vehicleTime)
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 36, 4, Passenger_km_in_day)
                    var_gpstaxi.writeData(var_gpstaxi.path_luutamthoi, "Sheet1", 4, 4, Passenger_address)
            except:
                break


        logging.info("Giám sát - Check thông tin: click vào xe - api - popup hiện trạng")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        logging.info("Pass")
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")


    async def Get_data_check_not_none(self, code, event, result, type, row, column):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        data = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', row, column)
        if type == 2:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {data}")
        if type == 3:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Api: {data}")
        if type == 4:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Popup hiện trạng: {data}")


        if (data == "") or (data == "None") or (data == None):
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")
        else:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")


    async def Get_data_check_can_none(self, code, event, type, result, row, column):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        data = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', row, column)
        if type == 2:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {data}")
        if type == 3:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Api: {data}")
        if type == 4:
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Popup hiện trạng: {data}")

        if (data == "") or (data == "None") or (data == None):
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")
        else:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")


    async def Get_data_check_address(self, code, event, result):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        web = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 4, 2)
        popup = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 4, 4)
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {web}\nPopup hiện trạng: {popup}")

        if popup in web:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")


    async def Get_data_check_seat(self, code, event, result):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        web = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 5, 2)
        api = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 5, 3)
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {web}\nApi: {api}")

        if api in web:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")


    async def Get_data_check_time(self, code, event, result):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        web = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 6, 2)
        api = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 6, 3)
        popup = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 6, 4)
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {web}\nApi: {api}\nPopup hiện trạng: {popup}")

        # web = "14:12:00 05/12/2025"
        # api = "14:12  05/12/2025"
        # popup = "14:14:23 05/12/2025"

        def parse_time(t):
            s = str(t).strip()
            # chuẩn hoá nhiều space -> 1 space
            s = re.sub(r'\s+', ' ', s)

            # danh sách format thử lần lượt (thường gặp)
            fmts = [
                "%H:%M:%S %d/%m/%Y",
                "%H:%M %d/%m/%Y",
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%H:%M:%S %Y-%m-%d",
                "%H:%M %Y-%m-%d",
            ]

            for f in fmts:
                try:
                    return datetime.strptime(s, f)
                except Exception:
                    pass

            # fallback: tách time + date bằng regex
            m = re.search(
                r'(\d{1,2}:\d{2}(?::\d{2})?)\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}|[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})',
                s)
            if m:
                time_part = m.group(1)
                date_part = m.group(2)

                # nếu time không có giây thì thêm :00
                if len(time_part.split(":")) == 2:
                    time_part = time_part + ":00"

                # chuẩn hoá date về dd/mm/YYYY
                if "-" in date_part and date_part.count("-") == 2 and date_part.startswith(tuple("0123456789")):
                    # có thể là YYYY-MM-DD hoặc D-M-YYYY; detect simple: nếu bắt đầu bởi 4 chữ số -> YYYY-MM-DD
                    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date_part):
                        y, mo, d = date_part.split("-")
                        date_part = f"{d.zfill(2)}/{mo.zfill(2)}/{y}"
                    else:
                        # D-M-YYYY -> chuyển sang dd/mm/YYYY
                        parts = date_part.split("-")
                        date_part = f"{parts[0].zfill(2)}/{parts[1].zfill(2)}/{parts[2]}"

                # nếu date dạng dd/mm/YYYY giữ nguyên
                try:
                    norm = f"{time_part} {date_part}"
                    return datetime.strptime(norm, "%H:%M:%S %d/%m/%Y")
                except Exception:
                    pass

            # nếu vẫn không parse được, raise để bạn biết dữ liệu lạ
            raise ValueError(f"Unrecognized datetime format: {t}")

        # chuyển về datetime
        t_web = parse_time(web)
        t_api = parse_time(api)
        t_popup = parse_time(popup)

        times = [t_web, t_api, t_popup]
        max_time = max(times)
        min_time = min(times)

        diff_minutes = (max_time - min_time).total_seconds() / 60

        if diff_minutes <= 3:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")
        print("Sai lệch:", diff_minutes, "phút")


    async def Get_data_check_v(self, code, event, result):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        web = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 10, 2)
        api = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 10, 3)
        popup = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 10, 4)
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Thông tin xe: {web}\nApi: {api}\nPopup hiện trạng: {popup}")


        # web = "48/49 Km/h"
        # api = "48"
        # popup = "46/46"

        def get_speed(val):
            val = str(val).strip()  # Ép về chuỗi để tránh lỗi int.split
            return int(val.split("/")[0].split()[0])

        # Lấy giá trị vận tốc dạng số
        s_web = get_speed(web)
        s_api = get_speed(api)
        s_popup = get_speed(popup)

        # Tính độ lệch lớn nhất
        speeds = [s_web, s_api, s_popup]
        diff = max(speeds) - min(speeds)

        # In ra giống format bạn yêu cầu
        if diff <= 10:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")


    async def Get_data_check_status(self, code, event, result):
        logging.info("Giám sát - Check thông tin xe")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        web = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 29, 2)
        api = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 29, 3)
        popup = var_gpstaxi.readData(var_gpstaxi.path_luutamthoi, 'Sheet1', 29, 4)
        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{web}\nApi: {api}\nPopup hiện trạng: {popup}")

        def extract(val):
            # Lấy chuỗi sau dấu ":" nếu có, còn không thì giữ nguyên
            if ":" in val:
                return val.split(":")[1].strip()
            return val.strip()

        # Chuẩn hoá 3 biến
        w = extract(web)
        a = extract(api)
        p = extract(popup)

        # So sánh
        if w == a == p:
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            logging.info("Fail")
            await self.page.screenshot(path=f"{imagepath}{code}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}.png")







    async def Right_mouse(self, type, name_button, check_button):
        await self.page.locator(f"xpath={var_gpstaxi.tblVehicleList2_2}").click(button="right")
        await asyncio.sleep(1.5)
        path_button1 = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-event')])[1]"
        path_button2 = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-event')])[2]"
        path_hover1 = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-text')])[1]"
        path_hover2 = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-text')])[2]"

        if type == "click":
            try:
                await self.page.click(f"xpath={path_button2}", timeout=1500)
            except:
                await self.page.click(f"xpath={path_button1}")
            await self.page.wait_for_selector(f"xpath={check_button}", timeout=5000)

        if type == "hover":
            try:
                button = self.page.locator(f"xpath={path_hover2}")
                await button.wait_for(state="attached", timeout=1500)
                await button.wait_for(state="visible", timeout=1500)
                await button.scroll_into_view_if_needed()
                await button.hover(force=True, timeout=1500)
                print("✅ đã hover phần tử 2")
            except Exception as e:
                print(path_hover2)
                print(f"❌ lỗi phần tử 2 (sau 1.5s): {e}")
            
            try:
                button = self.page.locator(f"xpath={path_hover1}")
                await button.wait_for(state="attached", timeout=1500)
                await button.wait_for(state="visible", timeout=1500)
                await button.scroll_into_view_if_needed()
                await button.hover(force=True, timeout=1500)
                print("✅ đã hover phần tử 1")
            except Exception as e:
                print(path_hover1)
                print(f"❌ lỗi phần tử 1 (sau 1.5s): {e}")


    async def Share_vehicle2(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await ListVehicle.Right_mouse(self, "click", "Chia sẻ phương tiện", var_gpstaxi.shareVehicleWindow_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Chuột phải xe - Chia sẻ phương tiện",
                                                                   var_gpstaxi.shareVehicleWindow_wnd_title, "Chia sẻ phương tiện", "_ChuotPhaiXe_ChiaSePhuongTien.png")

        try:
            await self.page.click(f"xpath={var_gpstaxi.shareVehicleWindow_wnd_title_x}")
            await asyncio.sleep(1)
        except:
            pass


    async def Review_the_route(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await ListVehicle.Right_mouse(self, "hover", "Xem lại lộ trình", "")

        logging.info(f"Giám sát - Xem lại lộ trình")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        time1 = await self.page.locator(f"xpath={var_gpstaxi.route_15p_name}").inner_text()
        time2 = await self.page.locator(f"xpath={var_gpstaxi.route_30p_name}").inner_text()
        time3 = await self.page.locator(f"xpath={var_gpstaxi.route_1h_name}").inner_text()
        time4 = await self.page.locator(f"xpath={var_gpstaxi.route_2h_name}").inner_text()
        time5 = await self.page.locator(f"xpath={var_gpstaxi.route_4h_name}").inner_text()
        time6 = await self.page.locator(f"xpath={var_gpstaxi.route_8h_name}").inner_text()
        time7 = await self.page.locator(f"xpath={var_gpstaxi.route_inday_name}").inner_text()
        time8 = await self.page.locator(f"xpath={var_gpstaxi.route_setting_name}").inner_text()

        logging.info(f"{time1}, {time2}, {time3}, {time4}, {time5}, {time6}")

        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{time1}, {time2}, {time3}, {time4}, {time5}, {time6}")

        if (time1 == "15 phút gần đây") and (time2 == "30 phút gần đây") and (time3 == "1h gần đây") and (time4 == "2h gần đây") \
            and (time5 == "4h gần đây") and (time6 == "8h gần đây") and (time7 == "Trong ngày") and (time8 == "Tùy chọn"):
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_XemLaiLoTrinh.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            logging.info("Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_XemLaiLoTrinh")


    async def Share_vehicle_route_8h_quickly(self, code, event, result):
        try:
            button = self.page.locator(f"xpath={var_gpstaxi.route_8h_name}")
            await button.scroll_into_view_if_needed()
            await button.hover(force=True, timeout=500)
            await asyncio.sleep(1)
        except:
            await ListVehicle.Review_the_route(self, "", "", "")
            button = self.page.locator(f"xpath={var_gpstaxi.route_8h_name}")
            await button.scroll_into_view_if_needed()
            await button.hover(force=True, timeout=500)
            await asyncio.sleep(1)


        await self.page.click(f"xpath={var_gpstaxi.see_quickly}", timeout=5000)
        await asyncio.sleep(1.5)

        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Xem lại lộ trình",
                                                          var_gpstaxi.icon_route1, "_XemLaiLoTrinh_8hGanDay_XemNhanh.png")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Xem lại lộ trình",
                                                                   var_gpstaxi.divDeleteWrapper_wnd_title, "Xóa Lộ trình", "_XemLaiLoTrinh_8hGanDay_XemNhanh.png")

        await self.page.click(f"xpath={var_gpstaxi.value_delete}")
        await asyncio.sleep(1)


    async def Share_vehicle_route_tab(self, code, event, result, link, path_check, desire, name_image):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await ListVehicle.Right_mouse(self, "hover", "Xem lại lộ trình", "")
        button = self.page.locator(f"xpath={var_gpstaxi.route_8h_name}")
        await button.scroll_into_view_if_needed()
        await button.hover(force=True, timeout=2000)
        await asyncio.sleep(1)

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Danh sách cảnh báo truyền C08 Bộ Công an",
                                                                link, path_check, desire, name_image)


    async def Status2(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        vehicle = await self.page.locator(f"xpath={var_gpstaxi.tblVehicleList2_2}").inner_text()
        await ListVehicle.Right_mouse(self, "click", "Hiện trạng", var_gpstaxi.VehicleStatus)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Chuột phải xe - Hiện trạng",
                                                                   var_gpstaxi.VehicleStatus, vehicle, "_ChuotPhaiXe_HienTrang.png")

        try:
            await self.page.click(f"xpath={var_gpstaxi.hide_detail_vehicle}")
            await asyncio.sleep(1)
        except:
            pass


    async def Info_devices(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")
        await ListVehicle.Right_mouse(self, "click", "Thông tin thiết bị", var_gpstaxi.divDeviceInfo)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Chuột phải xe - Thông tin thiết bị",
                                                                   var_gpstaxi.divDeviceInfo, "Thông tin thiết bị", "_ChuotPhaiXe_ThongTinThietBi.png")


    async def Info_devices_check_info(self, code, event, result, path_check, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={path_check}", timeout=300)
        except:
            await ListVehicle.Info_devices(self, "", "", "")

        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Chuột phải xe - Thông tin thiết bị",
                                                                   path_check, "", name_image)

        if name_image == "_ThongTinThietBi_TheNho.png":
            await self.page.click(f"xpath={var_gpstaxi.hide_info_devices}")
            await asyncio.sleep(1)


    async def Minitor_camera(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")
        await ListVehicle.Right_mouse(self, "hover", "Giám sát camera", "")

        await module_other_gpstaxi.write_result_text_content_handle(self.page, code, event, result, "Giám sát - Chuột phải xe - Giám sát camera",
                                                                    var_gpstaxi.Minitor_camera, var_gpstaxi.panel_review_title, " Giám sát camera",
                                                                    "_ChuotPhaiXe_GiamSatCarema.png")


    async def See_image_camera(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")
        await ListVehicle.Right_mouse(self, "click", "Xem ảnh camera", var_gpstaxi.wrong_date)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải xe - Xem ảnh camera",
                                                                    var_gpstaxi.wrong_date, "Không có dữ liệu", "_ChuotPhaiXe_XemAnhCarema.png")


    async def Subscriber_route(self, code, event, result):
        try:
            await self.page.wait_for_selector("xpath=//*[text()='Taxi Én Vàng [424]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await ListVehicle.Right_mouse(self, "hover", "Nhập thuê bao tuyến", "")

        async with self.page.context.expect_page() as new_page_info:
            await self.page.click(f"xpath={var_gpstaxi.Subscriber_route}")

        new_page = await new_page_info.value
        await new_page.wait_for_load_state("load", timeout=15000)

        # ✅ LƯU TAB VÀO SELF ĐỂ CASE 2 LẤY LẠI
        self.subscriber_page = new_page

        locator = new_page.locator(f"xpath={var_gpstaxi.panel_title}").first
        await locator.wait_for(state="visible", timeout=10000)

        check_text = await locator.text_content()
        module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 6, check_text)

        logging.info("Giám sát - Chuột phải xe - Nhập thuê bao tuyến")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        if "Nhập thuê bao tuyến" in check_text:
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
        else:
            await new_page.screenshot(path=f"{var_gpstaxi.imagepath}{code}_NhapThueBaoTuyen.png", full_page=True)
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 13, code + "_NhapThueBaoTuyen.png")


    async def Subscriber_route_fill(self, code, event, result):
        new_page = self.subscriber_page

        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}", timeout=500)

        except:
            await ListVehicle.Subscriber_route(self, "", "", "")

        await new_page.locator(f"xpath={var_gpstaxi.VehicleID_listbox}").click()
        await asyncio.sleep(1)
        await new_page.locator(f"xpath={var_gpstaxi.VehicleID_listbox1}").click()
        await asyncio.sleep(1)

        await new_page.locator(f"xpath={var_gpstaxi.DriverID_listbox}").click()
        await asyncio.sleep(1)
        await new_page.locator(f"xpath={var_gpstaxi.DriverID_listbox_1}").click()
        await asyncio.sleep(1)

        await new_page.locator(f"xpath={var_gpstaxi.StartAddressID_listbox}").click()
        await asyncio.sleep(1)
        await new_page.locator(f"xpath={var_gpstaxi.StartAddressID_listbox2}").click()
        await asyncio.sleep(1)

        await new_page.locator(f"xpath={var_gpstaxi.SubscriberTripID_listbox}").click()
        await asyncio.sleep(1)
        await new_page.locator(f"xpath={var_gpstaxi.SubscriberTripID_listbox2}").click()
        await asyncio.sleep(1)

        await new_page.locator(f"xpath={var_gpstaxi.WayType1}").click()
        await new_page.locator(f"xpath={var_gpstaxi.WayType2}").click()
        await asyncio.sleep(0.5)


        await new_page.fill(f"xpath={var_gpstaxi.SubscriberCost}", var_gpstaxi.data['minitor']['SubscriberCost'])

        await new_page.fill(f"xpath={var_gpstaxi.FromTime}", "07:00")
        await new_page.locator(f"xpath={var_gpstaxi.FromDate}").click()
        await asyncio.sleep(1)
        await new_page.keyboard.press("Enter")


        await new_page.locator(f"xpath={var_gpstaxi.PickUpKm_click}").click()
        await asyncio.sleep(1)
        await new_page.fill(f"xpath={var_gpstaxi.PickUpKm}", "25")


        #có thông tin trả khách
        await new_page.locator(f"xpath={var_gpstaxi.chkHasDropOff}").click()
        await asyncio.sleep(1.75)

        await new_page.fill(f"xpath={var_gpstaxi.ToTime}", "14:57")
        await new_page.locator(f"xpath={var_gpstaxi.ToDate_dateview}").click()
        await asyncio.sleep(1)
        await new_page.keyboard.press("Enter")

        await new_page.locator(f"xpath={var_gpstaxi.k_numeric2}").click()
        await asyncio.sleep(1)
        await new_page.fill(f"xpath={var_gpstaxi.DropOffKm}", "30")

        await new_page.locator(f"xpath={var_gpstaxi.k_numeric3}").click()
        await asyncio.sleep(1)
        await new_page.fill(f"xpath={var_gpstaxi.RealKm}", "80")

        await new_page.locator(f"xpath={var_gpstaxi.k_numeric4}").click()
        await asyncio.sleep(1)
        await new_page.fill(f"xpath={var_gpstaxi.MoneyMeter}", "240000")


        await new_page.locator(f"xpath={var_gpstaxi.OverPrice}").click()#Phụ trội lưu

        await new_page.locator(f"xpath={var_gpstaxi.k_numeric5}").click()
        await asyncio.sleep(1)
        await new_page.locator(f"xpath={var_gpstaxi.MoneyReceiver}").click()

        await new_page.fill(f"xpath={var_gpstaxi.Note}", "Trường test nhập thuê bao tuyến")
        await new_page.wait_for_selector(f"xpath={var_gpstaxi.order_async}")

        logging.info("Giám sát - Chuột phải xe - Nhập thuê bao tuyến")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        logging.info("Pass")
        module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")


    async def Subscriber_route_check(self, code, event, result, path_check, desire, name_image):
        new_page = self.subscriber_page

        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}", timeout=500)

        except:
            await ListVehicle.Subscriber_route(self, "", "", "")

        logging.info("Giám sát - Chuột phải xe - Nhập thuê bao tuyến")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            locator = new_page.locator(f"xpath={path_check}")
            check_text = await locator.input_value(timeout=1500)
            logging.info(f"TextContent: {check_text}")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, check_text)

            if check_text == desire:
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
                logging.info("Pass")
            else:
                await new_page.screenshot(path=f"{imagepath}{code}{name_image}.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await new_page.screenshot(path=f"{imagepath}{code}{name_image}.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")


    async def Subscriber_route_cancel(self, code, event, result):
        new_page = self.subscriber_page
        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}", timeout=500)

        except:
            await ListVehicle.Subscriber_route(self, "", "", "")

        await new_page.fill(f"xpath={var_gpstaxi.SubscriberCost}", var_gpstaxi.data['minitor']['SubscriberCost'])
        await asyncio.sleep(1)

        await new_page.locator(f"xpath={var_gpstaxi.btnAbort}").click()
        await asyncio.sleep(1.5)

        logging.info("Giám sát - Chuột phải xe - Nhập thuê bao tuyến")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        try:
            locator = new_page.locator(f"xpath={var_gpstaxi.SubscriberCost}")
            check_text = await locator.input_value(timeout=1500)
            logging.info(f"TextContent: {check_text}")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, check_text)

            if check_text != var_gpstaxi.data['minitor']['SubscriberCost']:
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
                logging.info("Pass")
            else:
                await new_page.screenshot(path=f"{imagepath}{code}_NhapThueBaoTuyen_HuyBo.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_NhapThueBaoTuyen_HuyBo")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await new_page.screenshot(path=f"{imagepath}{code}_NhapThueBaoTuyen_HuyBo.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_NhapThueBaoTuyen_HuyBo")

        await new_page.close()


    async def Driver_call(self, code, event, result):
        try:
            new_page = self.subscriber_page
            await new_page.close()
        except:
            pass

        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                            var_gpstaxi.data['login']['binhthuong_mk'])

        await ListVehicle.Right_mouse(self, "hover", "Lái xe báo", "")

        logging.info(f"Giám sát - Chuột phải xe - Lái xe báo")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        Driver_call1 = await self.page.locator(f"xpath={var_gpstaxi.Driver_call1_name}").inner_text()
        Driver_call2 = await self.page.locator(f"xpath={var_gpstaxi.Driver_call2_name}").inner_text()

        logging.info(f"{Driver_call1}, {Driver_call2}")

        module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{Driver_call1}, {Driver_call2}")

        if (Driver_call1 == "Báo nghỉ") and (Driver_call2 == "Xe hoạt động lại"):
            logging.info("Pass")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
        else:
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_LaiXeBao.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            logging.info("Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_LaiXeBao")

        await self.page.click(f"xpath={var_gpstaxi.Driver_call1_button}")


    async def Driver_call_button(self, code, event, result, button, name_image):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await ListVehicle.Right_mouse(self, "hover", "Lái xe báo", "")
        await self.page.click(f"xpath={button}")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải xe - Lái xe báo",
                                                                var_gpstaxi.update_success, "Cập nhật dữ liệu thành công", name_image)


    async def Hide_vehicle(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await ListVehicle.Right_mouse(self, "click", "Ẩn xe", var_gpstaxi.vehiclesHiddenAddWindow_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải xe - Ẩn xe",
                                                                    var_gpstaxi.vehiclesHiddenAddWindow_wnd_title, "Ẩn xe", "_ChuotPhaiXe_AnXe.png")

        try:
            await self.page.click(f"xpath={var_gpstaxi.vehiclesHiddenAddWindow_wnd_title_x}")
            await asyncio.sleep(1)
        except:
            pass


    async def Route(self, code, event, result):
        await self.login_page.goto("Mã XN", "424", "Taxi Én Vàng [424]")

        await self.page.click(f"xpath={var_gpstaxi.tabstrip_2}")
        await asyncio.sleep(1)

        await self.page.click(f"xpath={var_gpstaxi.VehiclePlate_listbox}")
        await asyncio.sleep(1.5)

        number = await self.page.locator(f"xpath={var_gpstaxi.VehiclePlate_listbox1}").text_content()
        await self.page.click(f"xpath={var_gpstaxi.VehiclePlate_listbox1}")
        await asyncio.sleep(1)

        await module_other_gpstaxi.write_result_text_content_handle_value(self.page, code, event, result, "Giám sát - Chuột phải xe - Ẩn xe",
                                                                          var_gpstaxi.get_data,  var_gpstaxi.VehiclePlate_input,
                                                                          number, "_DanhSachXe_LoTrinh.png")



class Map:

    def __init__(self, page):
        self.page = page
        self.login_page = Login(page)


    async def Right_map(self, name_button, check_button):
        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
        await asyncio.sleep(1.5)

        path_button = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-event')])[1]"
        # path_name = f"(//div[contains(@class,'x-menu-item') and .//div[normalize-space()='{name_button}']]  //div[contains(@class,'x-menu-items-text')])[1]"

        await self.page.click(f"xpath={path_button}")
        await self.page.wait_for_selector(f"xpath={check_button}", timeout=5000)


    async def Search_curent_vehicle(self, code, event, result):
        await self.login_page.goto("Mã XN", "6072", "Công ty Xuân Thành [6072]")

        await Map.Right_map(self, "Tìm xe gần nhất", var_gpstaxi.divNearestWrapper_wnd_title)
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Tìm xe gần nhất",
                                                                    var_gpstaxi.divNearestWrapper_wnd_title, "Tìm xe gần nhất", "_ChuotPhaiMap_TimXeGanNhat.png")


    async def Search_curent_vehicle_button(self, code, event, result, button, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.ddlSortCarNearest_listbox}", timeout=250)
        except:
            await Map.Search_curent_vehicle(self, "", "", "")
            await self.page.click(f"xpath={var_gpstaxi.ddlSortCarNearest_listbox}")

        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={button}")
        await asyncio.sleep(2)

        logging.info("Giám sát - Chuột phải map - Tìm xe gần nhất")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            divNearest1_1 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_1}").inner_text()
            divNearest1_2 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_2}").inner_text()
            divNearest1_3 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_3}").inner_text()
            divNearest1_4 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_4}").inner_text()
            divNearest1_5 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_5}").inner_text()
            divNearest1_6 = await self.page.locator(f"xpath={var_gpstaxi.divNearest1_6}").inner_text()

            logging.info(f"Số hiệu xe: {divNearest1_1}\n"
                         f"Khoảng cách (km): {divNearest1_2}\n"
                         f"Dự kiến (phút): {divNearest1_3}\n"
                         f"Doanh thu trong ngày: {divNearest1_4}\n"
                         f"Thời gian dừng đỗ (giờ:phút): {divNearest1_5}\n"
                         f"Xe di chuyển đón khách: {divNearest1_6}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                                           f"Số hiệu xe: {divNearest1_1}\n"
                                           f"Khoảng cách (km): {divNearest1_2}\n"
                                           f"Dự kiến (phút): {divNearest1_3}\n"
                                           f"Doanh thu trong ngày: {divNearest1_4}\n"
                                           f"Thời gian dừng đỗ (giờ:phút): {divNearest1_5}\n"
                                           f"Xe di chuyển đón khách: {divNearest1_6}")

            if (divNearest1_1 != "") and (divNearest1_2 != "") and (divNearest1_3 != "") \
                    and (divNearest1_4 != "") and (divNearest1_5 != "") and (divNearest1_6 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")


        if name_image == "_TimXeGanNhat_KhoangCach.png":
            try:
                await self.page.click(f"xpath={var_gpstaxi.divNearestWrapper_wnd_title_x}")
                await asyncio.sleep(1.5)
            except:
                pass


    async def Find_forgotten_items(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Công ty Xuân Thành [6072]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "6072", "Công ty Xuân Thành [6072]")

        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
        await asyncio.sleep(1.5)


        async with self.page.context.expect_page() as new_page_info:
            await self.page.click(f"xpath={var_gpstaxi.Find_forgotten_items}")

        new_page = await new_page_info.value
        await new_page.wait_for_load_state("load", timeout=15000)

        self.Find_forgotten_items = new_page

        locator = new_page.locator(f"xpath={var_gpstaxi.findCarWindow_wnd_title}").first
        await locator.wait_for(state="visible", timeout=10000)

        check_text = await locator.text_content()
        module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 6, check_text)

        logging.info("Giám sát - Chuột phải map - Tìm đồ khách quên")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        if "Tìm xe" in check_text:
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
        else:
            await new_page.screenshot(path=f"{var_gpstaxi.imagepath}{code}_TimDoKhachQuen.png", full_page=True)
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 13, code + "_TimDoKhachQuen.png")


    async def Find_forgotten_items_search(self, code, event, result):
        new_page = self.Find_forgotten_items
        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.findCarWindow_wnd_title}", timeout=500)

        except:
            await Map.Find_forgotten_items(self, "", "", "")

        await new_page.locator(f"xpath={var_gpstaxi.Find_forgotten_items_search}").click()
        await asyncio.sleep(2)
        logging.info("Giám sát - Chuột phải map - Tìm xe gần nhất")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            rowgroup1_1 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_1}").inner_text()
            rowgroup1_2 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_2}").inner_text()
            rowgroup1_3 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_3}").inner_text()
            rowgroup1_4 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_4}").inner_text()
            rowgroup1_5 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_5}").inner_text()
            rowgroup1_6 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_6}").inner_text()
            rowgroup1_7 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_7}").inner_text()
            rowgroup1_8 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_8}").inner_text()
            rowgroup1_9 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_9}").inner_text()
            rowgroup1_10 = await new_page.locator(f"xpath={var_gpstaxi.rowgroup1_10}").inner_text()

            logging.info(f"SHX: {rowgroup1_1}\n"
                         f"Biển số: {rowgroup1_2}\n"
                         f"Lái xe: {rowgroup1_3}\n"
                         f"Giờ lên: {rowgroup1_4}\n"
                         f"Giờ xuống: {rowgroup1_5}\n"
                         f"Địa chỉ lên: {rowgroup1_6}\n"
                         f"Địa chỉ xuống: {rowgroup1_7}\n"
                         f"Số tiền: {rowgroup1_8}\n"
                         f"Xem nhanh: {rowgroup1_9}\n"
                         f"Xem lộ trình ở trang khác: {rowgroup1_10}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6,
                                           f"SHX: {rowgroup1_1}\n"
                                           f"Biển số: {rowgroup1_2}\n"
                                           f"Lái xe: {rowgroup1_3}\n"
                                           f"Giờ lên: {rowgroup1_4}\n"
                                           f"Giờ xuống: {rowgroup1_5}\n"
                                           f"Địa chỉ lên: {rowgroup1_6}\n"
                                           f"Địa chỉ xuống: {rowgroup1_7}\n"
                                           f"Số tiền: {rowgroup1_8}\n"
                                           f"Xem nhanh: {rowgroup1_9}\n"
                                           f"Xem lộ trình ở trang khác: {rowgroup1_10}")

            if (rowgroup1_1 != "") and (rowgroup1_2 != "") and (rowgroup1_4 != "") \
                    and (rowgroup1_5 != "") and (rowgroup1_6 != "") and (rowgroup1_7 != "")\
                    and (rowgroup1_8 != "") and (rowgroup1_9 == "Xem") and (rowgroup1_10 == "Xem"):
                logging.info("Pass")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_TimDoKhachQuen_TimKiem.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_TimDoKhachQuen_TimKiem.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_TimDoKhachQuen_TimKiem.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_TimDoKhachQuen_TimKiem.png")

        await new_page.close()


    async def List_driver_not_login(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='Công ty Xuân Thành [6072]']", timeout=500)
        except:
            await self.login_page.goto("Mã XN", "6072", "Công ty Xuân Thành [6072]")


        await Map.Right_map(self, "Danh sách lái xe chưa đăng nhập", var_gpstaxi.divListDriverNotLoginWrapper_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Danh sách lái xe chưa đăng nhập",
                                                                    var_gpstaxi.divListDriverNotLoginWrapper_wnd_title, "Danh sách lái xe chưa đăng nhập",
                                                                "_ChuotPhaiMap_DanhSachLaiXeChuaDangNhap.png")


    async def List_driver_not_login_group(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicle}",  timeout=500)
        except:
            await Map.List_driver_not_login(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.txtTreeView}")
        await asyncio.sleep(1.5)

        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result,
                                                                      "Giám sát - Chuột phải map - Danh sách lái xe chưa đăng nhập",
                                                                      var_gpstaxi.List_driver_not_login_group,  "",
                                                                      "_DanhSachLaiXeChuaDangNhap_NhomDoi.png")
        await self.page.click(f"xpath={var_gpstaxi.fa_fa_times}")
        await asyncio.sleep(1)


    async def List_driver_not_login_number(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicle}",  timeout=500)
        except:
            await Map.List_driver_not_login(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.txtTreeView}")
        await asyncio.sleep(1.5)


        number = await self.page.locator(f"xpath={var_gpstaxi.divListDriverNotLogin2_2}").inner_text()
        await self.page.type(f"xpath={var_gpstaxi.acVehicle}", number)
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.acVehicle_listbox1}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.update_data}")
        await asyncio.sleep(1.5)
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Danh sách lái xe chưa đăng nhập",
                                                                    var_gpstaxi.divListDriverNotLogin1_2, number, "_DanhSachLaiXeChuaDangNhap_SoHieuXe.png")


    async def List_driver_not_login_update_data(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicle}",  timeout=500)
        except:
            await Map.List_driver_not_login(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.update_data}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.update_success}", timeout=5000)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Danh sách lái xe chưa đăng nhập",
                                                                    var_gpstaxi.update_success, "Cập nhật thành công", "_DanhSachLaiXeChuaDangNhap_CapNhatDuLieu.png")


    async def List_driver_not_login_excel(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.acVehicle}",  timeout=500)
        except:
            await Map.List_driver_not_login(self, "", "", "")


        await module_other_gpstaxi.write_result_web_excel(self.page, code, event, result, "Danh sách lái xe chưa đăng nhập - Xuất excel",
                                                      var_gpstaxi.ExportExcelDriverNotLogin, "//*[@id='divListDriverNotLoginHead']//table[2]/tbody/tr/td",
                                                      "//*[@id='divListDriverNotLogin']//table[1]/tbody/tr/td", 5, 8)


    async def Add_a_marker(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
        await asyncio.sleep(1.5)

        async with self.page.context.expect_page() as new_page_info:
            await self.page.click(f"xpath={var_gpstaxi.Add_a_marker}")

        new_page = await new_page_info.value
        await new_page.wait_for_load_state("load", timeout=15000)

        self.Add_a_marker = new_page

        locator = new_page.locator(f"xpath={var_gpstaxi.window_wnd_title}").first
        await locator.wait_for(state="visible", timeout=10000)

        check_text = await locator.text_content()
        module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 6, check_text)

        logging.info("Giám sát - Chuột phải map - Tạo điểm bản đồ")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")

        if "Thêm mới Điểm, vùng" in check_text:
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
        else:
            await new_page.screenshot(path=f"{var_gpstaxi.imagepath}{code}_TaoDiemBanDo.png", full_page=True)
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 13, code + "_TaoDiemBanDo.png")


    async def Add_a_marker_save(self, code, event, result):
        new_page = self.Add_a_marker
        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.window_wnd_title}", timeout=500)

        except:
            await Map.Add_a_marker(self, "", "", "")


        await new_page.fill(f"xpath={var_gpstaxi.Name}", var_gpstaxi.data['minitor']['Name'])
        await new_page.fill(f"xpath={var_gpstaxi.PrivateName}", var_gpstaxi.data['minitor']['PrivateName'])
        await new_page.click(f"xpath={var_gpstaxi.FK_LandmarkCategoryID_option_selected}")
        await asyncio.sleep(2)
        try:
            await new_page.click(f"xpath={var_gpstaxi.park}", timeout=2000)
            await asyncio.sleep(1.5)
        except:
            await new_page.click(f"xpath={var_gpstaxi.FK_LandmarkCategoryID_option_selected}")
            await asyncio.sleep(2)
            try:
                await new_page.click(f"xpath={var_gpstaxi.park}", timeout=2000)
                await asyncio.sleep(1.5)
            except:
                pass

        await new_page.click(f"xpath={var_gpstaxi.IsPolygon2}")
        await new_page.click(f"xpath={var_gpstaxi.optionInsert1}")
        await asyncio.sleep(2)

        # await new_page.fill(f"xpath={var_gpstaxi.txtAddressSuggest}", var_gpstaxi.data['minitor']['txtAddressSuggest'])
        await new_page.wait_for_selector(f"xpath={var_gpstaxi.txtAddressSuggest}")

        await new_page.fill(f"xpath={var_gpstaxi.Longitude}", var_gpstaxi.data['minitor']['Longitude'])
        await new_page.fill(f"xpath={var_gpstaxi.Latitude}", var_gpstaxi.data['minitor']['Latitude'])
        await new_page.fill(f"xpath={var_gpstaxi.Radius}", var_gpstaxi.data['minitor']['Radius'])
        await new_page.click(f"xpath={var_gpstaxi.IsLandmarkManagement}")
        await new_page.click(f"xpath={var_gpstaxi.IsVisible}")
        await new_page.fill(f"xpath={var_gpstaxi.PhoneNumber_input}", var_gpstaxi.data['minitor']['PhoneNumber_input'])
        await new_page.fill(f"xpath={var_gpstaxi.Email}", var_gpstaxi.data['minitor']['Email'])
        await new_page.fill(f"xpath={var_gpstaxi.Description}", var_gpstaxi.data['minitor']['Description'])
        await new_page.fill(f"xpath={var_gpstaxi.HighWayVelocityAllow}", var_gpstaxi.data['minitor']['HighWayVelocityAllow'])
        await new_page.fill(f"xpath={var_gpstaxi.LowWayVelocityAllow}", var_gpstaxi.data['minitor']['LowWayVelocityAllow'])
        await new_page.click(f"xpath={var_gpstaxi.IsHallAlert}")
        await new_page.fill(f"xpath={var_gpstaxi.MinVehicle}", var_gpstaxi.data['minitor']['MinVehicle'])
        await new_page.fill(f"xpath={var_gpstaxi.MaxVehicle}", var_gpstaxi.data['minitor']['MaxVehicle'])
        await new_page.click(f"xpath={var_gpstaxi.IsLongInAreaAlert}")
        await new_page.fill(f"xpath={var_gpstaxi.MinuteLongAreaAlert}", var_gpstaxi.data['minitor']['MinuteLongAreaAlert'])
        await asyncio.sleep(1.5)

        await new_page.click(f"xpath={var_gpstaxi.btnSubmit}")
        await new_page.wait_for_selector(f"xpath={var_gpstaxi.update_success}")
        await module_other_gpstaxi.write_result_text_inner_text_in(new_page, code, event, result, "Giám sát - Chuột phải map - Tạo điểm bản đồ",
                                                                    var_gpstaxi.update_success, "Thêm mới thành công", "_TaoDiemBanDo_ThemMoi.png")


    async def Add_a_marker_update(self, code, event, result):
        new_page = self.Add_a_marker
        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.map_icon_park}", timeout=500)

        except:
            await Map.Add_a_marker_save(self, "", "", "")

        await new_page.click(f"xpath={var_gpstaxi.map_icon_park}")
        await new_page.fill(f"xpath={var_gpstaxi.Name}", var_gpstaxi.data['minitor']['Name_edit'])
        await asyncio.sleep(2.5)
        await new_page.click(f"xpath={var_gpstaxi.btnSubmit}")
        await new_page.wait_for_selector(f"xpath={var_gpstaxi.update_success}")
        await module_other_gpstaxi.write_result_text_inner_text_in(new_page, code, event, result, "Giám sát - Chuột phải map - Tạo điểm bản đồ",
                                                                    var_gpstaxi.update_success, "Cập nhật dữ liệu thành công", "_TaoDiemBanDo_CapNhat.png")


    async def Add_a_marker_delete(self, code, event, result):
        new_page = self.Add_a_marker
        try:
            await new_page.wait_for_selector(f"xpath={var_gpstaxi.map_icon_park}", timeout=500)

        except:
            await Map.Add_a_marker_save(self, "", "", "")

        await new_page.click(f"xpath={var_gpstaxi.map_icon_park}")
        await asyncio.sleep(2.5)
        new_page.context.once("dialog", lambda d: d.accept())#alert
        await new_page.click(f"xpath={var_gpstaxi.Add_a_marker_delete}")

        await module_other_gpstaxi.write_result_text_inner_text_in(new_page, code, event, result, "Giám sát - Chuột phải map - Tạo điểm bản đồ",
                                                                    var_gpstaxi.update_success, "Xóa thành công", "_TaoDiemBanDo_Xoa.png")
        await new_page.close()


    async def See_address(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox}")
        await self.page.click(f"xpath={var_gpstaxi.ddlSearchProperty_listbox_coordinates}")

        await self.page.type(f"xpath={var_gpstaxi.txtPointSearch}", var_gpstaxi.data['minitor']['coordinates1'])
        await self.page.click(f"xpath={var_gpstaxi.btnVehicleSearch}")

        await asyncio.sleep(1.5)
        await Map.Right_map(self, "Xem địa chỉ", var_gpstaxi.check_Search_landmark)
        await asyncio.sleep(1.5)
        logging.info("Giám sát - Chuột phải map - Xem địa chỉ")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            locator1 = self.page.locator(f"xpath={var_gpstaxi.check_Search_landmark}")
            locator2 = self.page.locator(f"xpath={var_gpstaxi.check_Search_coordinates}")

            check_text1 = await locator1.inner_text()
            check_text2 = await locator2.inner_text()
            logging.info(f"{check_text1}\n{check_text2}")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"{check_text1}\n{check_text2}")

            if ("Nguyễn Khoái, P. Vĩnh Hưng, TP. Hà Nội" in check_text1) and ("Kinh độ : 105" in check_text2):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_XemDiaChi.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_XemDiaChi.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_GiamSat_XemDiaChi.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_GiamSat_XemDiaChi.png")

        await self.page.click(f"xpath={var_gpstaxi.close_button}")


    async def Measure_distance1(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await Map.Right_map(self, "Đo khoảng cách", var_gpstaxi.distanceWindow_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Đo khoảng cách",
                                                                    var_gpstaxi.distanceWindow_wnd_title, "Đo khoảng cách", "_ChuotPhaiMap_DoKhoangCach.png")


        await self.page.click(f"xpath={var_gpstaxi.distanceWindow_wnd_title_x}")


    async def Navigation(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
        await asyncio.sleep(1.5)

        await module_other_gpstaxi.write_result_text_content_handle_title(self.page, code, event, result, "Giám sát - Chuột phải map - Dẫn đường",
                                                                          var_gpstaxi.Navigation, "Google Maps",  "_ChuotPhaiMap_DanDuong.png")


    async def Garage_vehicles(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        await Map.Right_map(self, "Xem xe trong gara", var_gpstaxi.divGaraWrapper_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Xem xe trên gara",
                                                                    var_gpstaxi.divGaraWrapper_wnd_title, "Tìm xe trong gara", "_ChuotPhaiMap_XemXeTrenGara.png")


    async def Garage_vehicles_checkinfo(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.divGaraWrapper_wnd_title}",  timeout=500)
        except:
            await Map.Navigation(self, "", "", "")


        logging.info("Giám sát - Chuột phải map - Xem xe trên gara")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            divGara1_1 = await self.page.locator(f"xpath={var_gpstaxi.divGara1_1}").inner_text()
            divGara1_2 = await self.page.locator(f"xpath={var_gpstaxi.divGara1_2}").inner_text()
            divGara1_3 = await self.page.locator(f"xpath={var_gpstaxi.divGara1_3}").inner_text()

            logging.info(f"Tên gara: {divGara1_1}\nDanh sách xe: {divGara1_2}\nTổng: {divGara1_3}")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Tên gara: {divGara1_1}\nDanh sách xe: {divGara1_2}\nTổng: {divGara1_3}")

            if (divGara1_1 != "") and (divGara1_2 != "") and (divGara1_3 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_XemXeTrenGara_CheckThongTin.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_XemXeTrenGara_CheckThongTin.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_XemXeTrenGara_CheckThongTin.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_XemXeTrenGara_CheckThongTin.png")

        await self.page.click(f"xpath={var_gpstaxi.divGaraWrapper_wnd_title_x}")


    async def Find_vehicles_stop(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[batest424]-[424] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                                var_gpstaxi.data['login']['batest424_mk'])


        await Map.Right_map(self, "Tìm xe dừng đỗ trong vùng ĐH", var_gpstaxi.divVehiclesInOperateAreaWrapper_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Tìm xe dừng đỗ trong vùng ĐH",
                                                                    var_gpstaxi.divVehiclesInOperateAreaWrapper_wnd_title, "Tìm xe dừng đỗ trong vùng ĐH",
                                                                "_ChuotPhaiMap_TimXeDungDoTrongVungDieuHanh.png")


    async def Find_vehicles_stop_checkbox(self, code, event, result, type_checkbox, name_image):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[batest424]-[424] ']", timeout=500)
        except:
            await Map.Find_vehicles_stop(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.ddlOperateAreas_listbox}")
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.ddlOperateAreas_listbox2}")
        await asyncio.sleep(1.5)

        checkbox = self.page.locator(var_gpstaxi.cbInOutOperateAreas)
        checked = await checkbox.is_checked()

        if type_checkbox == "Yes" and not checked:
            await checkbox.click()

        if type_checkbox == "No" and checked:
            await checkbox.click()
        await asyncio.sleep(2)


        logging.info("Giám sát - Chuột phải map - Tìm xe dừng đỗ trong vùng ĐH")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            divInOperateArea1_1 = await self.page.locator(f"xpath={var_gpstaxi.divInOperateArea1_1}").inner_text()
            divInOperateArea1_2 = await self.page.locator(f"xpath={var_gpstaxi.divInOperateArea1_2}").inner_text()
            divInOperateArea1_3 = await self.page.locator(f"xpath={var_gpstaxi.divInOperateArea1_3}").inner_text()
            divInOperateArea1_4 = await self.page.locator(f"xpath={var_gpstaxi.divInOperateArea1_4}").inner_text()


            logging.info(f"Số hiệu xe: {divInOperateArea1_1}\n"
                         f"Biển số xe: {divInOperateArea1_2}\n"
                         f"Doanh thu trong ngày: {divInOperateArea1_3}\n"
                         f"Thời gian dừng đỗ/Thời gian xe trong vùng (phút): {divInOperateArea1_4}")

            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"Số hiệu xe: {divInOperateArea1_1}\n"
                                                                                f"Biển số xe: {divInOperateArea1_2}\n"
                                                                                f"Doanh thu trong ngày: {divInOperateArea1_3}\n"
                                                                                f"Thời gian dừng đỗ (phút): {divInOperateArea1_4}")

            if (divInOperateArea1_1 != "") and (divInOperateArea1_2 != "") and (divInOperateArea1_3 != "") and (divInOperateArea1_4 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}{name_image}", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}{name_image}")


        if name_image == "_TimXeDungDoTrongVungDH_TichChon.png":
            await self.page.click(f"xpath={var_gpstaxi.divVehiclesInOperateAreaWrapper_wnd_title_x}")


    async def Find_vehicles_in_the_zone(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.Find_vehicles_in_the_zone}")
        await asyncio.sleep(1.5)
        await self.page.locator(f"xpath={var_gpstaxi.Find_vehicles_in_the_zone1}").click(button="left", force=True)
        await asyncio.sleep(1)
        await self.page.locator(f"xpath={var_gpstaxi.Find_vehicles_in_the_zone2}").click(button="left", force=True)
        await asyncio.sleep(1)
        await self.page.locator(f"xpath={var_gpstaxi.Find_vehicles_in_the_zone3}").dblclick(force=True)
        await asyncio.sleep(1.5)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Tìm xe trong vùng",
                                                                    var_gpstaxi.divAreaWrapper_wnd_title, "Tìm xe trong vùng",
                                                                "_ChuotPhaiMap_TimXeTrongVung.png")


    async def Find_vehicles_in_the_zone_checkinfo(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.divAreaWrapper_wnd_title}")
        except:
            await Map.Find_vehicles_in_the_zone(self, "", "", "")


        logging.info("Giám sát - Chuột phải map - Tìm xe trong vùng")
        logging.info(f"Mã - {code}")
        logging.info(f"Tên sự kiện - {event}")
        logging.info(f"Kết quả - {result}")
        try:
            divArea1_1 = await self.page.locator(f"xpath={var_gpstaxi.divArea1_1}").inner_text()
            divArea1_2 = await self.page.locator(f"xpath={var_gpstaxi.divArea1_2}").inner_text()
            divArea1_3 = await self.page.locator(f"xpath={var_gpstaxi.divArea1_3}").inner_text()
            divArea1_4 = await self.page.locator(f"xpath={var_gpstaxi.divArea1_4}").inner_text()

            logging.info(f"STT: {divArea1_1}\nSố xe: {divArea1_2}\nVận tốc: {divArea1_3}\nĐịa chỉ: {divArea1_4}")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, f"STT: {divArea1_1}\nSố xe: {divArea1_2}"
                                                                                f"\nVận tốc: {divArea1_3}\nĐịa chỉ: {divArea1_4}")

            if (divArea1_1 != "") and (divArea1_2 != "") and (divArea1_3 != "") and (divArea1_4 != ""):
                logging.info("Pass")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            else:
                logging.info("Fail")
                await self.page.screenshot(path=f"{imagepath}{code}_TimXeTrongvung_CheckThongTin.png", full_page=True)
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_TimXeTrongvung_CheckThongTin.png")
        except Exception as e:
            logging.info(f"Fail - {e}")
            await self.page.screenshot(path=f"{imagepath}{code}_TimXeTrongvung_CheckThongTin.png", full_page=True)
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Fail")
            module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 13, f"{code}_TimXeTrongvung_CheckThongTin.png")

        await self.page.click(f"xpath={var_gpstaxi.divAreaWrapper_wnd_title_x}")


    async def Toggle_point_zones(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])



        await Map.Right_map(self, "Ẩn hiện vùng , điểm", var_gpstaxi.LandMarkConfig_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Ẩn hiện vùng , điểm",
                                                                    var_gpstaxi.LandMarkConfig_wnd_title, "Cấu hình hiển thị điểm - vùng",
                                                                "_ChuotPhaiMap_AnHienVungDiem.png")


    async def Toggle_point_zones_checkbox(self, code, event, result, type_checkbox, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.chkIsShowLabel}", timeout=500)
        except:
            await Map.Toggle_point_zones(self, "", "", "")


        checkbox = self.page.locator(var_gpstaxi.chkIsShowLabel)
        checked = await checkbox.is_checked()

        if type_checkbox == "Yes" and not checked:
            await checkbox.click()

        if type_checkbox == "No" and checked:
            await checkbox.click()
        await asyncio.sleep(2)

        await self.page.click(f"xpath={var_gpstaxi.btnAccept}")

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Ẩn hiện vùng , điểm",
                                                                    var_gpstaxi.update_success, "Cập nhật dữ liệu thành công", name_image)


    async def Show_hide_boundary(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])

        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.Show_hide_boundary}", timeout=500)

            await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
            await asyncio.sleep(1.5)
            await self.page.click(f"xpath={var_gpstaxi.Show_hide_boundary_button}")
            await asyncio.sleep(1.5)

            await module_other_gpstaxi.write_result_not_displayed(self.page, code, event, result,  "Giám sát - Chuột phải map - Ẩn/hiện đường bao",
                                                              var_gpstaxi.Show_hide_boundary, "_ChuotPhaiMap_AnHienVungBao.png")
        except:
            await self.page.click(f"xpath={var_gpstaxi.basic_map}", button="right", position={"x": 470, "y": 450})
            await asyncio.sleep(1.5)
            await self.page.click(f"xpath={var_gpstaxi.Show_hide_boundary_button}")
            await asyncio.sleep(1.5)

            await module_other_gpstaxi.write_result_displayed(self.page, code, event, result,  "Giám sát - Chuột phải map - Ẩn/hiện đường bao",
                                                              var_gpstaxi.Show_hide_boundary, "_ChuotPhaiMap_AnHienVungBao.png")


    async def Startup_configuration(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath=//*[text()='[auto_binhthuong]-[999998] ']", timeout=500)
        except:
            await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['binhthuong_tk'],
                                                var_gpstaxi.data['login']['binhthuong_mk'])


        await Map.Right_map(self, "Cấu hình khởi động", var_gpstaxi.configOnlineDiv_wnd_title)

        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Cấu hình khởi động",
                                                                    var_gpstaxi.configOnlineDiv_wnd_title, "Cấu hình bản đồ", "_ChuotPhaiMap_CauHinhKhoiDong.png")


    async def Startup_configuration_type(self, code, event, result, name_map, name_image):
        try:
            await self.page.click(f"xpath={var_gpstaxi.zoom_input}",  timeout=500)
        except:
            await Map.Startup_configuration(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.type_map}")
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath=//*[@id='Map_listbox']//*[text()='{name_map}']")
        await asyncio.sleep(2)

        await self.page.click(f"xpath={var_gpstaxi.longitude_click}")
        await self.page.fill(f"xpath={var_gpstaxi.longitude_input}", "105,847692")

        await self.page.click(f"xpath={var_gpstaxi.latitude_click}")
        await self.page.fill(f"xpath={var_gpstaxi.latitude_input}", "20,982286")


        await self.page.click(f"xpath={var_gpstaxi.zoom_input}")
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.zoom_input14}")
        await asyncio.sleep(1.5)
        await self.page.click(f"xpath={var_gpstaxi.btnMapConfigSave}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Giám sát - Chuột phải map - Cấu hình khởi động",
                                                                    var_gpstaxi.update_success, "Cập nhật dữ liệu thành công", name_image)
        await asyncio.sleep(2)



class Monitor_multiple_vehicles:


    def __init__(self, page):
        self.page = page
        self.login_page = Login(page)


    async def Monitor_multiple_vehicles_x(self, number):
        n = number
        while n:
            try:
                await self.page.click(f"xpath=(//i[contains(@class,'icon-remove-circle')])[{str(n)}]", timeout=200)
            except:
                pass
            n -= 1


    async def Monitor_multiple_vehicles(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        await self.page.click(f"xpath={var_gpstaxi.minitor}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_vehicles1}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_VehicleStatus}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.check_VehicleStatus, "Hiện trạng xe", "_GiamSat_GiamSatNhieuXe.png")


    async def Monitor_3_vehicles(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.remove_circle1}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Monitor_multiple_vehicles(self, "", "", "")

        await Monitor_multiple_vehicles.Monitor_multiple_vehicles_x(self, 5)

        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList1_1}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList2_1}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList3_1}")
        await asyncio.sleep(2)
        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.Monitor_multiple_x3, "_GiamSatNhieuXe_Chon3xe.png")

        await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_x3}")
        await asyncio.sleep(1)
        await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_x2}")
        await asyncio.sleep(1)


    async def Monitor_1_vehicles(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.remove_circle1}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Monitor_multiple_vehicles(self, "", "", "")

        await Monitor_multiple_vehicles.Monitor_multiple_vehicles_x(self, 5)

        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList1_1}")
        await asyncio.sleep(2)
        await module_other_gpstaxi.write_result_displayed(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.Monitor_multiple_x1, "_GiamSatNhieuXe_Chon1xe_a.png")

        await module_other_gpstaxi.write_result_not_displayed(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.Monitor_multiple_x2, "_GiamSatNhieuXe_Chon1xe_b.png")


    async def Zoom_in(self, code, event, result):
        try:
            await self.page.click(f"xpath={var_gpstaxi.remove_circle1}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Monitor_multiple_vehicles(self, "", "", "")

        await Monitor_multiple_vehicles.Monitor_multiple_vehicles_x(self, 5)

        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList1_1}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_zoomin1}")
        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.CurrentStatus, "", "_GiamSatNhieuXe_PhongTo.png")
        try:
            await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_x2}")
            await asyncio.sleep(1)
        except:
            pass


    async def Close(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.remove_circle1}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Monitor_1_vehicles(self, "", "", "")

        await Monitor_multiple_vehicles.Monitor_multiple_vehicles_x(self, 5)

        await self.page.click(f"xpath={var_gpstaxi.tblVehicleList1_1}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Monitor_multiple_x1}")
        await asyncio.sleep(1)
        await module_other_gpstaxi.write_result_not_displayed(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.Monitor_multiple_x1, "_GiamSatNhieuXe_Dong.png")


    async def Number_LiscensePlate(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.remove_circle1}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Monitor_1_vehicles(self, "", "", "")

        number = await self.page.locator(f"xpath={var_gpstaxi.tblVehicleList1_2a}").inner_text(timeout=3000)

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    var_gpstaxi.check_VehicleStatus, number, "_GiamSatNhieuXe_SoHieuBienSo.png")






    async def Check_info_status_path(self, code, event, result, type, path_check, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_VehicleStatus}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Number_LiscensePlate(self, "", "", "")

        try:
            await self.page.wait_for_selector(f"xpath={path_check}", timeout=500)
        except:
            if type == 1:
                await self.page.click(f"xpath={var_gpstaxi.status}")
            if type == 2:
                await self.page.click(f"xpath={var_gpstaxi.info_bgt}")
            await asyncio.sleep(2)

        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                    path_check, "", name_image)


    async def Check_info_status_tab1_name(self, code, event, result, desire_name, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_VehicleStatus}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Number_LiscensePlate(self, "", "", "")


        n = 1
        while (n < 25):
            n = n + 1
            path_name = f"(//div[contains(@id,'lstData')])/div[{str(n)}]/div[1]"
            path_data = f"(//div[contains(@id,'lstData')])/div[{str(n)}]/div[2]"
            try:
                name = await self.page.locator(f"xpath={path_name}").inner_text(timeout=300)
                if name == desire_name:
                    data = await self.page.locator(f"xpath={path_data}").inner_text(timeout=300)
                    print(f"name: {name}, data: {data}")
                    await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                                  path_data, "", name_image)
                    break
                else:
                    module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 6, "Không hiển thị")
                    module_other_gpstaxi.writeData(checklistpath, "Checklist", code, 7, "Pass")
            except:
                pass


    async def Check_info_status_tab2_name(self, code, event, result, desire_name, name_image):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_VehicleStatus}", timeout=500)
        except:
            await Monitor_multiple_vehicles.Number_LiscensePlate(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.info_bgt}")
        if name_image == "_GiamSatNhieuXe_SoVin.png":
            await asyncio.sleep(2)

        n = 0
        while (n < 10):
            n = n + 1
            path_name = f"(//article[contains(@id,'tab2')])/div[{str(n)}]/div[1]"
            path_data = f"(//article[contains(@id,'tab2')])/div[{str(n)}]/div[2]"
            try:
                name = await self.page.locator(f"xpath={path_name}").inner_text(timeout=300)
                if name == desire_name:
                    data = await self.page.locator(f"xpath={path_data}").inner_text(timeout=300)
                    print(f"name: {name}, data: {data}")
                    await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Giám sát - Giám sát nhiều xe",
                                                                                  path_data, "", name_image)
                    break
            except:
                pass






