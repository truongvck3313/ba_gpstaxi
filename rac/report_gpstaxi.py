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





class Report:


    def __init__(self, page):
        self.page = page
        self.login_page = Login(page)


    async def Detailed_trip_report_by_vehicle(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        button = self.page.locator(f"xpath={var_gpstaxi.report}")
        await button.wait_for(state="attached", timeout=1500)
        await button.wait_for(state="visible", timeout=1500)
        await button.scroll_into_view_if_needed()
        await button.hover(force=True, timeout=1500)
        # await self.page.click(f"xpath={var_gpstaxi.report}")
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Detailed_trip_report_by_vehicle}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo chi tiết cuốc khách theo xe",
                                                                   var_gpstaxi.panel_title, "BÁO CÁO CHI TIẾT CUỐC KHÁCH THEO XE", "_BaoCaoChiTietCuocKhachTheoXe.png")


    async def Detailed_trip_report_by_vehicle_search(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.from_money}", timeout=500)
        except:
            await Report.Detailed_trip_report_by_vehicle(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnSearch}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid2_1}")
        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo chi tiết cuốc khách theo xe",
                                                                   var_gpstaxi.DisplayGrid1_3, "", "_BaoCaoChiTietCuocKhachTheoXe_TimKiem.png")


    async def Detailed_trip_report_by_vehicle_report(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.from_money}", timeout=500)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid1_2}", timeout=500)
        except:
            await Report.Detailed_trip_report_by_vehicle_search(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.Print_report}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.reportWindow_wnd_title}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo chi tiết cuốc khách theo xe",
                                                                   var_gpstaxi.reportWindow_wnd_title, "Báo cáo chi tiết cuốc khách theo xe", "_BaoCaoChiTietCuocKhachTheoXe_BaoCao.png")

        await self.page.click(f"xpath={var_gpstaxi.reportWindow_wnd_title_x}")
        await asyncio.sleep(2)


    async def Detailed_trip_report_by_vehicle_excel(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.from_money}", timeout=500)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid1_2}", timeout=500)
        except:
            await Report.Detailed_trip_report_by_vehicle_search(self, "", "", "")


        await module_other_gpstaxi.write_result_web_excel_display(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo chi tiết cuốc khách theo xe",
                                                      var_gpstaxi.export_excel, "//*[@id='DisplayGrid']//table/thead//th",
                                                       "//*[@id='DisplayGrid']//table/tbody/tr[1]/td", 3, 4, skip_column="Lộ trình")








    async def Summary_trip_report_by_vehicle(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        button = self.page.locator(f"xpath={var_gpstaxi.report}")
        await button.wait_for(state="attached", timeout=1500)
        await button.wait_for(state="visible", timeout=1500)
        await button.scroll_into_view_if_needed()
        await button.hover(force=True, timeout=1500)
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Summary_trip_report_by_vehicle}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo tổng hợp cuốc khách theo xe",
                                                                   var_gpstaxi.panel_title, "BÁO CÁO TỔNG HỢP CUỐC KHÁCH THEO XE", "_BaoCaoTongHopCuocKhachTheoXe.png")


    async def Summary_trip_report_by_vehicle_search(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.persent_guest}", timeout=500)
        except:
            await Report.Summary_trip_report_by_vehicle(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnSearch}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid2_1}")
        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo tổng hợp cuốc khách theo xe",
                                                                   var_gpstaxi.DisplayGrid1_3, "", "_BaoCaoTongHopCuocKhachTheoXe_TimKiem.png")


    async def Summary_trip_report_by_vehicle_report(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.persent_guest}", timeout=500)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid1_2}", timeout=500)
        except:
            await Report.Summary_trip_report_by_vehicle_search(self, "", "", "")


        await self.page.click(f"xpath={var_gpstaxi.Print_report}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.reportWindow_wnd_title}")
        await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo tổng hợp cuốc khách theo xe",
                                                                   var_gpstaxi.reportWindow_wnd_title, "In báo cáo", "_BaoCaoTongHopCuocKhachTheoXe_BaoCao.png")

        await self.page.click(f"xpath={var_gpstaxi.reportWindow_wnd_title_x}")
        await asyncio.sleep(2)


    async def Summary_trip_report_by_vehicle_excel(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.persent_guest}", timeout=500)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid1_2}", timeout=500)
        except:
            await Report.Summary_trip_report_by_vehicle_search(self, "", "", "")


        await module_other_gpstaxi.write_result_web_excel(self.page, code, event, result, "Báo cáo - DOANH THU & HIỆU SUẤT KINH DOANH - Báo cáo tổng hợp cuốc khách theo xe",
                                                      var_gpstaxi.export_excel, "//*[@id='DisplayGrid']//table/thead//*[@class='k-header']",
                                                       "//*[@id='DisplayGrid']//table/tbody/tr[1]//*[@role='gridcell']", 3, 4)










    async def Speeding_report(self, code, event, result):
        await self.login_page.login_gpstaxi(var_gpstaxi.data['login']['batest424_tk'],
                                            var_gpstaxi.data['login']['batest424_mk'])

        button = self.page.locator(f"xpath={var_gpstaxi.report}")
        await button.wait_for(state="attached", timeout=1500)
        await button.wait_for(state="visible", timeout=1500)
        await button.scroll_into_view_if_needed()
        await button.hover(force=True, timeout=1500)
        await asyncio.sleep(2)
        await self.page.click(f"xpath={var_gpstaxi.Speeding_report}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.panel_title}")

        await module_other_gpstaxi.write_result_text_inner_text_in(self.page, code, event, result, "Báo cáo - BÁO CÁO HOẠT ĐỘNG XE - Báo cáo quá tốc độ",
                                                                   var_gpstaxi.panel_title, "BÁO CÁO QUÁ TỐC ĐỘ", "_BaoCaoQuaTocDo.png")


    async def Speeding_report_search(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.speeding}", timeout=500)
        except:
            await Report.Speeding_report(self, "", "", "")

        await self.page.click(f"xpath={var_gpstaxi.btnSearch}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid2_1}")
        await module_other_gpstaxi.write_result_text_inner_text_other(self.page, code, event, result, "Báo cáo - BÁO CÁO HOẠT ĐỘNG XE - Báo cáo quá tốc độ",
                                                                   var_gpstaxi.DisplayGrid1_3, "", "_BaoCaoQuaTocDo_TimKiem.png")


    async def Speeding_report_excel(self, code, event, result):
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.speeding}", timeout=500)
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.DisplayGrid1_2}", timeout=500)
        except:
            await Report.Speeding_report_search(self, "", "", "")


        await module_other_gpstaxi.write_result_web_excel_display(self.page, code, event, result, "Báo cáo - BÁO CÁO HOẠT ĐỘNG XE - Báo cáo quá tốc độ",
                                                      var_gpstaxi.export_excel, "//*[@id='DisplayGrid']//table/thead//*[@class='k-header']",
                                                       "//*[@id='DisplayGrid']//table/tbody/tr[1]//*[@role='gridcell']", 3, 4, skip_column="Lộ trình")







