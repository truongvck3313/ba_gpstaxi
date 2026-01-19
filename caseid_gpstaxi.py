import openpyxl
import var_gpstaxi
import login_gpstaxi
import minitor_gpstaxi
import route_gpstaxi
import report_gpstaxi



# Hàm lấy dữ liệu từ Excel1
def get_datachecklist(code):
    workbook = openpyxl.load_workbook(var_gpstaxi.checklistpath)
    sheet = workbook["Checklist"]
    rownum = 9
    while rownum < 3000:
        rownum += 1
        if sheet[f"A{rownum}"].value == code:
            event = sheet[f"B{rownum}"].value
            result = sheet[f"E{rownum}"].value
            return event, result
    return None, None


class CaseID:
    def __init__(self, page):
        self.page = page
        self.icon_page = minitor_gpstaxi.IconPage(page)
        self.login_page = login_gpstaxi.Login(page)
        self.link_page = login_gpstaxi.Link(page)
        self.list_vehicle = minitor_gpstaxi.ListVehicle(page)
        self.map = minitor_gpstaxi.Map(page)
        self.multiple_vehicles = minitor_gpstaxi.Monitor_multiple_vehicles(page)
        self.route = route_gpstaxi.Route(page)
        self.report = report_gpstaxi.Report(page)




    async def Login01(self):
        event, result = get_datachecklist("Login01")
        await self.login_page.check_login("Login01", event, result, 1,
        var_gpstaxi.data['login']['binhanh_tk'], var_gpstaxi.data['login']['binhanh_mk'],
        var_gpstaxi.check_goto, "Công ty Bình Anh", "_DangNhap_TaiKhoanBinhAnh.png")


    async def Login02(self):
        # Chưa có logic, để trống
        pass


    async def Login03(self):
        event, result = get_datachecklist("Login03")
        await self.login_page.check_login("Login03", event, result, 2,
        var_gpstaxi.data['login']['binhthuong_tk'], var_gpstaxi.data['login']['binhthuong_mk'],
        var_gpstaxi.minitor_vehicle1,  "", "_DangNhap_TaiKhoanBinhThuong.png")


    async def Login04(self):
        event, result = get_datachecklist("Login04")
        await self.login_page.check_login("Login04", event, result, 2,
        var_gpstaxi.data['login']['laixe_tk'], var_gpstaxi.data['login']['laixe_mk'],
        var_gpstaxi.minitor_vehicle1, "", "_DangNhap_TaiKhoanLaiXe.png")


    async def Login05(self):
        event, result = get_datachecklist("Login05")
        await self.login_page.check_login("Login05", event, result, 2,
        var_gpstaxi.data['login']['quanlynhanuoc_tk'], var_gpstaxi.data['login']['quanlynhanuoc_mk'],
        var_gpstaxi.minitor_vehicle1, "", "_DangNhap_QuanLyNhaNuoc.png")


    async def Login06(self):
        event, result = get_datachecklist("Login06")
        await self.login_page.check_login("Login06", event, result, 2,
        var_gpstaxi.data['login']['quantri_tk'], var_gpstaxi.data['login']['quantri_mk'],
        var_gpstaxi.minitor_vehicle1, "", "_DangNhap_TaiKhoanQuanTri.png")


    async def Login07(self):
        event, result = get_datachecklist("Login07")
        await self.login_page.check_login("Login07", event, result, 0,
        var_gpstaxi.data['login']['khongcoquyengiamsat_tk'], var_gpstaxi.data['login']['khongcoquyengiamsat_mk'],
        var_gpstaxi.minitor, "", "_DangNhap_TaiKhoanKhongCoQuyenGiamSat.png")


    async def Login08(self):
        event, result = get_datachecklist("Login08")
        await self.login_page.wrong_login("Login08", event, result)


    async def Login09(self):
        event, result = get_datachecklist("Login09")
        await self.login_page.remember_to_log_in("Login09", event, result, checkbox=True)


    async def Login10(self):
        event, result = get_datachecklist("Login10")
        await self.login_page.remember_to_log_in("Login10", event, result, checkbox=False)


    async def Login11(self):
        event, result = get_datachecklist("Login11")
        await self.login_page.forgot_password("Login11", event, result)


    async def Login12(self):
        event, result = get_datachecklist("Login12")
        await self.link_page.check_link("Login12", event, result, 1,
        var_gpstaxi.icon_home, "", "https://bagps.vn/", "_DangNhap_IconTrangChu.png")


    async def Login13(self):
        event, result = get_datachecklist("Login13")
        await self.link_page.check_link("Login13", event, result, 0,
        "", var_gpstaxi.icon_sdt, " 19006415", "_DangNhap_SoDienThoai.png")


    async def Login14(self):
        event, result = get_datachecklist("Login14")
        await self.link_page.check_link("Login14", event, result, 1,
        var_gpstaxi.icon_bagps, "", "https://bagps.vn/", "_DangNhap_IconBagps.png")


    async def Login15(self):
        event, result = get_datachecklist("Login15")
        await self.link_page.check_link("Login15", event, result, 2,
        var_gpstaxi.icon_chplay, var_gpstaxi.check_icon_chplay, "BA Taxi", "_DangNhap_IconChPlay.png")


    async def Login16(self):
        event, result = get_datachecklist("Login16")
        await self.link_page.check_link("Login16", event, result, 2,
        var_gpstaxi.icon_appstore, var_gpstaxi.check_icon_appstore, "BA TAXI", "_DangNhap_IconAppStore.png")


    async def Login17(self):
        event, result = get_datachecklist("Login17")
        await self.link_page.check_link("Login17", event, result, 1,
        var_gpstaxi.information_and_solutions, "", "https://bagps.vn/san-pham-va-giai-phap", "_DangNhap_ThongTinVaGiaiPhap.png")


    async def Login18(self):
        event, result = get_datachecklist("Login18")
        await self.link_page.check_link("Login18", event, result, 1,
        var_gpstaxi.about_us, "", "https://bagps.vn/gioi-thieu/", "_DangNhap_VeChungToi.png")


    async def Login19(self):
        event, result = get_datachecklist("Login19")
        await self.link_page.check_link("Login19", event, result, 1,
        var_gpstaxi.network, "", "https://bagps.vn/mang-luoi", "_DangNhap_MangLuoi.png")


    async def Login20(self):
        event, result = get_datachecklist("Login20")
        await self.link_page.check_link("Login20", event, result, 1,
        var_gpstaxi.use_help, "", "https://www.youtube.com/channel", "_DangNhap_HuongDanSuDung.png")


    async def Login21(self):
        event, result = get_datachecklist("Login21")
        await self.link_page.check_link("Login21", event, result, 1,
        var_gpstaxi.fee_help, "", "https://bagps.vn/huong-dan-dong-phi-dich-vu-ba-gps", "_DangNhap_HuongDanDongPhi.png")


    async def Login22(self):
        event, result = get_datachecklist("Login22")
        await self.link_page.check_link("Login22", event, result, 1,
        var_gpstaxi.info_gtvt, "", "https://bagps.vn/category/tin-tuc/", "_DangNhap_TinTucNghanhGTVT.png")


    async def Minitor01(self):
        event, result = get_datachecklist("Minitor01")
        await self.icon_page.icon_zoom("Minitor01", event, result,
        var_gpstaxi.icon_zoom_in, "_GiamSat_IconPhongTo.png")


    async def Minitor02(self):
        event, result = get_datachecklist("Minitor02")
        await self.icon_page.icon_zoom("Minitor02", event, result,
        var_gpstaxi.icon_zoom_out, "_GiamSat_IconPhongThuNho.png")


    async def Minitor03(self):
        event, result = get_datachecklist("Minitor03")
        await self.icon_page.select_map("Minitor03", event, result)


    async def Minitor04(self):
        event, result = get_datachecklist("Minitor04")
        await self.icon_page.c08_bca("Minitor04", event, result)


    async def Minitor05(self):
        event, result = get_datachecklist("Minitor05")
        await self.icon_page.c08_bca_link("Minitor05", event, result, var_gpstaxi.c08_company, var_gpstaxi.check_c08_company,
                                          "Đơn vị kinh doanh vận tải", "_DanhSachCanhBaoTruyenC08BCA_ThongTinDoanhNghiep.png")


    async def Minitor06(self):
        event, result = get_datachecklist("Minitor06")
        await self.icon_page.c08_bca_link("Minitor06", event, result, var_gpstaxi.c08_vehicle, var_gpstaxi.check_c08_vehicle,
                                          "Loại hình kinh doanh", "_DanhSachCanhBaoTruyenC08BCA_ThongTinXe.png")


    async def Minitor07(self):
        event, result = get_datachecklist("Minitor07")
        await self.icon_page.c08_bca_link("Minitor07", event, result, var_gpstaxi.c08_driver, var_gpstaxi.check_c08_driver,
                                          "Loại bằng", "_DanhSachCanhBaoTruyenC08BCA_ThongTinLaiXe.png")


    async def Minitor08(self):
        event, result = get_datachecklist("Minitor08")
        await self.icon_page.c08_bca_refresh("Minitor08", event, result)


    async def Minitor09(self):
        event, result = get_datachecklist("Minitor09")
        await self.icon_page.c08_bca_group("Minitor09", event, result)


    async def Minitor10(self):
        event, result = get_datachecklist("Minitor10")
        await self.icon_page.c08_bca_vehicle("Minitor10", event, result)


    async def Minitor11(self):
        event, result = get_datachecklist("Minitor11")
        await self.icon_page.c08_bca_check_info("Minitor11", event, result)


    async def Minitor12(self):
        event, result = get_datachecklist("Minitor12")
        await self.icon_page.c08_bca_icon_transmission("Minitor12", event, result)


    async def Minitor13(self):
        event, result = get_datachecklist("Minitor13")
        await self.icon_page.c08_bca_displayed("Minitor13", event, result, var_gpstaxi.list_bca_1_8_input, "_C08BCA_XacNhanBoTruyen.png")


    async def Minitor14(self):
        event, result = get_datachecklist("Minitor14")
        await self.icon_page.c08_bca_displayed("Minitor14", event, result, var_gpstaxi.cbx_accept, "_C08BCA_ToiCamKetThongTin.png")


    async def Minitor15(self):
        event, result = get_datachecklist("Minitor15")
        await self.icon_page.c08_bca_displayed("Minitor15", event, result, var_gpstaxi.save_missing, "_C08BCA_Luu.png")


    async def Minitor16(self):
        event, result = get_datachecklist("Minitor16")
        await self.icon_page.c08_bca_close("Minitor16", event, result)


    async def Minitor17(self):
        event, result = get_datachecklist("Minitor17")
        await self.icon_page.hidden_car_list("Minitor17", event, result)


    async def Minitor18(self):
        event, result = get_datachecklist("Minitor18")
        await self.icon_page.hidden_car_list_add_new("Minitor18", event, result)


    async def Minitor19(self):
        event, result = get_datachecklist("Minitor19")
        await self.icon_page.hidden_car_list_vehicle("Minitor19", event, result)


    async def Minitor20(self):
        event, result = get_datachecklist("Minitor20")
        await self.icon_page.hidden_car_list_resson("Minitor20", event, result)


    async def Minitor21(self):
        event, result = get_datachecklist("Minitor21")
        await self.icon_page.hidden_car_list_status("Minitor21", event, result)


    async def Minitor22(self):
        event, result = get_datachecklist("Minitor22")
        await self.icon_page.hidden_car_list_permission("Minitor22", event, result)


    async def Minitor23(self):
        event, result = get_datachecklist("Minitor23")
        await self.icon_page.hidden_car_list_fee("Minitor23", event, result)


    async def Minitor24(self):
        event, result = get_datachecklist("Minitor24")
        await self.icon_page.hidden_car_lis_check_info("Minitor24", event, result)


    async def Minitor25(self):
        event, result = get_datachecklist("Minitor25")
        await self.icon_page.hidden_car_lis_history("Minitor25", event, result)


    async def Minitor26(self):
        event, result = get_datachecklist("Minitor26")
        await self.icon_page.hidden_car_lis_cancel("Minitor26", event, result)


    async def Minitor27(self):
        event, result = get_datachecklist("Minitor27")
        await self.icon_page.Search("Minitor27", event, result)


    async def Minitor28(self):
        event, result = get_datachecklist("Minitor28")
        await self.icon_page.Monitor_multiple_vehicles("Minitor28", event, result)


    async def Minitor29(self):
        event, result = get_datachecklist("Minitor29")
        await self.icon_page.Measure_distance("Minitor29", event, result)


    async def Minitor30(self):
        event, result = get_datachecklist("Minitor30")
        await self.icon_page.Measure_distance_select_2_point("Minitor30", event, result)


    async def Minitor31(self):
        event, result = get_datachecklist("Minitor31")
        await self.icon_page.Measure_distance_check("Minitor31", event, result, var_gpstaxi.distance_km, "_DoKhoangCach_Km.png")


    async def Minitor32(self):
        event, result = get_datachecklist("Minitor32")
        await self.icon_page.Measure_distance_check("Minitor32", event, result, var_gpstaxi.distance_m, "_DoKhoangCach_Met.png")


    async def Minitor33(self):
        event, result = get_datachecklist("Minitor33")
        await self.icon_page.Measure_distance_check("Minitor33", event, result, var_gpstaxi.distance_dam, "_DoKhoangCach_Dam.png")


    async def Minitor34(self):
        event, result = get_datachecklist("Minitor34")
        await self.icon_page.Measure_distance_reset("Minitor34", event, result)


    async def Minitor35(self):
        event, result = get_datachecklist("Minitor35")
        await self.icon_page.Guide("Minitor35", event, result)


    async def Minitor36(self):
        event, result = get_datachecklist("Minitor36")
        await self.icon_page.Check_fee("Minitor36", event, result)


    async def Minitor37(self):
        event, result = get_datachecklist("Minitor37")
        await self.icon_page.Check_fee_payment("Minitor37", event, result)


    async def Minitor38(self):
        event, result = get_datachecklist("Minitor38")
        await self.icon_page.Make_an_appointment("Minitor38", event, result)


    async def Minitor39(self):
        event, result = get_datachecklist("Minitor39")
        await self.icon_page.Make_an_appointment_fill("Minitor39", event, result)


    async def Minitor40(self):
        event, result = get_datachecklist("Minitor40")
        await self.icon_page.Make_an_appointment_checkbutton("Minitor40", event, result, var_gpstaxi.btnSubmitForm,
                                                             "Lưu và trở về", "_DatLichHen_LuuVaTroVe.png")


    async def Minitor41(self):
        event, result = get_datachecklist("Minitor41")
        await self.icon_page.Make_an_appointment_checkbutton("Minitor41", event, result, var_gpstaxi.btnSubmitFormContinue,
                                                             "Lưu và tiếp tục", "_DatLichHen_LuuVaTiepTuc.png")


    async def Minitor42(self):
        event, result = get_datachecklist("Minitor42")
        await self.icon_page.Make_an_appointment_exit("Minitor42", event, result)


    async def Minitor43(self):
        event, result = get_datachecklist("Minitor43")
        await self.icon_page.Appointment_list("Minitor43", event, result)


    async def Minitor44(self):
        event, result = get_datachecklist("Minitor44")
        await self.icon_page.Lobby_area_warning("Minitor44", event, result)


    async def Minitor45(self):
        event, result = get_datachecklist("Minitor45")
        await self.icon_page.Lobby_area_warning_area("Minitor45", event, result)


    async def Minitor46(self):
        event, result = get_datachecklist("Minitor46")
        await self.icon_page.Lobby_area_warning_lobby("Minitor46", event, result)


    async def Minitor47(self):
        event, result = get_datachecklist("Minitor47")
        await self.icon_page.Lobby_area_warning_suburb("Minitor47", event, result)


    async def Minitor48(self):
        event, result = get_datachecklist("Minitor48")
        await self.icon_page.Lobby_area_warning_update("Minitor48", event, result)


    async def Minitor49(self):
        event, result = get_datachecklist("Minitor49")
        await self.icon_page.Lobby_area_warning_exit("Minitor49", event, result)


    async def Minitor50(self):
        event, result = get_datachecklist("Minitor50")
        await self.list_vehicle.ListVehicle_combobox("Minitor50", event, result, "Giám sát - Nhóm đội", var_gpstaxi.Online_VehicleGroup_listbox,
                                                     var_gpstaxi.Online_VehicleGroup_listbox2, "_GiamSat_NhomDoi.png")


    async def Minitor51(self):
        event, result = get_datachecklist("Minitor51")
        await self.list_vehicle.ListVehicle_combobox("Minitor51", event, result, "Giám sát - Trạng Thái", var_gpstaxi.Online_VehicleStatus_listbox,
                                                     var_gpstaxi.Online_VehicleStatus_listbox2, "_GiamSat_TrangThai.png")

    async def Minitor52(self):
        event, result = get_datachecklist("Minitor52")
        await self.list_vehicle.Search_vehicle("Minitor52", event, result)


    async def Minitor53(self):
        event, result = get_datachecklist("Minitor53")
        await self.list_vehicle.Search_address("Minitor53", event, result)


    async def Minitor54(self):
        event, result = get_datachecklist("Minitor54")
        await self.list_vehicle.Search_landmark("Minitor54", event, result)


    async def Minitor55(self):
        event, result = get_datachecklist("Minitor55")
        await self.list_vehicle.Search_coordinates("Minitor55", event, result)


    async def Minitor56(self):
        event, result = get_datachecklist("Minitor56")
        await self.list_vehicle.Status("Minitor56", event, result, "no_group",
                                       "- Hoạt động ", "_KhongNhom_HoatDong.png")


    async def Minitor57(self):
        event, result = get_datachecklist("Minitor57")
        await self.list_vehicle.Status("Minitor57", event, result, "no_group",
                                       " -- Có khách", "_KhongNhom_CoKhach.png")


    async def Minitor58(self):
        event, result = get_datachecklist("Minitor58")
        await self.list_vehicle.Status("Minitor58", event, result, "no_group",
                                       " -- Không khách", "_KhongNhom_KhongKhach.png")


    async def Minitor59(self):
        event, result = get_datachecklist("Minitor59")
        await self.list_vehicle.Status("Minitor59", event, result, "no_group",
                                       " -- Di chuyển", "_KhongNhom_DiChuyen.png")


    async def Minitor60(self):
        event, result = get_datachecklist("Minitor60")
        await self.list_vehicle.Status("Minitor60", event, result, "no_group",
                                       " -- Dừng đỗ", "_KhongNhom_DungDo.png")


    async def Minitor61(self):
        event, result = get_datachecklist("Minitor61")
        await self.list_vehicle.Status("Minitor61", event, result, "no_group",
                                       " -- Nổ máy", "_KhongNhom_NoMay.png")


    async def Minitor62(self):
        event, result = get_datachecklist("Minitor62")
        await self.list_vehicle.Status("Minitor62", event, result, "no_group",
                                       " -- Tắt máy", "_KhongNhom_TatMay.png")


    async def Minitor63(self):
        event, result = get_datachecklist("Minitor63")
        await self.list_vehicle.Status("Minitor63", event, result, "no_group",
                                       "- Mất tín hiệu", "_KhongNhom_MatTinHieu.png")


    async def Minitor64(self):
        event, result = get_datachecklist("Minitor64")
        await self.list_vehicle.Status("Minitor64", event, result, "no_group",
                                       "- Khóa đồng hồ", "_KhongNhom_KhoaDongHo.png")


    async def Minitor65(self):
        event, result = get_datachecklist("Minitor65")
        await self.list_vehicle.Status("Minitor65", event, result, "no_group",
                                       "- Mất kết nối đồng hồ", "_KhongNhom_MatKetNoiDongHo.png")


    async def Minitor66(self):
        event, result = get_datachecklist("Minitor66")
        await self.list_vehicle.Status("Minitor66", event, result, "no_group",
                                       "Tất cả", "_KhongNhom_TatCa.png")







    async def Minitor67(self):
        event, result = get_datachecklist("Minitor67")
        await self.list_vehicle.Status("Minitor67", event, result, "have_group",
                                       "- Hoạt động ", "_CoNhom_HoatDong.png")


    async def Minitor68(self):
        event, result = get_datachecklist("Minitor68")
        await self.list_vehicle.Status("Minitor68", event, result, "have_group",
                                       " -- Có khách", "_CoNhom_CoKhach.png")


    async def Minitor69(self):
        event, result = get_datachecklist("Minitor69")
        await self.list_vehicle.Status("Minitor69", event, result, "have_group",
                                       " -- Không khách", "_CoNhom_KhongKhach.png")


    async def Minitor70(self):
        event, result = get_datachecklist("Minitor70")
        await self.list_vehicle.Status("Minitor70", event, result, "have_group",
                                       " -- Di chuyển", "_CoNhom_DiChuyen.png")


    async def Minitor71(self):
        event, result = get_datachecklist("Minitor71")
        await self.list_vehicle.Status("Minitor71", event, result, "have_group",
                                       " -- Dừng đỗ", "_CoNhom_DungDo.png")


    async def Minitor72(self):
        event, result = get_datachecklist("Minitor72")
        await self.list_vehicle.Status("Minitor72", event, result, "have_group",
                                       " -- Nổ máy", "_CoNhom_NoMay.png")


    async def Minitor73(self):
        event, result = get_datachecklist("Minitor73")
        await self.list_vehicle.Status("Minitor73", event, result, "have_group",
                                       " -- Tắt máy", "_CoNhom_TatMay.png")


    async def Minitor74(self):
        event, result = get_datachecklist("Minitor74")
        await self.list_vehicle.Status("Minitor74", event, result, "have_group",
                                       "- Mất tín hiệu", "_CoNhom_MatTinHieu.png")


    async def Minitor75(self):
        event, result = get_datachecklist("Minitor75")
        await self.list_vehicle.Status("Minitor75", event, result, "have_group",
                                       "- Báo nghỉ", "_CoNhom_BaoNghi.png")



    async def Minitor76(self):
        event, result = get_datachecklist("Minitor76")
        await self.list_vehicle.Status("Minitor76", event, result, "have_group",
                                       "- Khóa đồng hồ", "_CoNhom_KhoaDongHo.png")


    async def Minitor77(self):
        event, result = get_datachecklist("Minitor77")
        await self.list_vehicle.Status("Minitor77", event, result, "have_group",
                                       "- Mất kết nối đồng hồ", "_CoNhom_MatKetNoiDongHo.png")


    async def Minitor78(self):
        event, result = get_datachecklist("Minitor78")
        await self.list_vehicle.Status("Minitor78", event, result, "have_group",
                                       "Tất cả", "_CoNhom_TatCa.png")


    async def Minitor79(self):
        event, result = get_datachecklist("Minitor79")
        await self.list_vehicle.Icon_refresh("Minitor79", event, result)


    async def Minitor80(self):
        event, result = get_datachecklist("Minitor80")
        await self.list_vehicle.System_status("Minitor80", event, result)


    async def Minitor81(self):
        event, result = get_datachecklist("Minitor81")
        await self.list_vehicle.System_status_check("Minitor81", event, result, "Có khách", "Passenger", "_HienTrangHeThong_CoKhach.png")


    async def Minitor82(self):
        event, result = get_datachecklist("Minitor82")
        await self.list_vehicle.System_status_check("Minitor82", event, result, "Không khách", "EmptyPassenger", "_HienTrangHeThong_KhongKhach.png")


    async def Minitor83(self):
        event, result = get_datachecklist("Minitor83")
        await self.list_vehicle.System_status_check("Minitor83", event, result, "Mất tín hiệu", "LostSignal", "_HienTrangHeThong_MatTinHieu.png")


    async def Minitor84(self):
        event, result = get_datachecklist("Minitor84")
        await self.list_vehicle.System_status_list_vehicle_active("Minitor84", event, result)


    async def Minitor85(self):
        event, result = get_datachecklist("Minitor85")
        await self.list_vehicle.System_status_check("Minitor85", event, result, "Tắt máy", "MachineOff", "_HienTrangHeThong_TatMay.png")


    async def Minitor86(self):
        event, result = get_datachecklist("Minitor86")
        await self.list_vehicle.System_status_check("Minitor86", event, result, "Quá tốc độ", "SpeedOver", "_HienTrangHeThong_QuaTocDo.png")


    async def Minitor87(self):
        event, result = get_datachecklist("Minitor87")
        await self.list_vehicle.System_status_check("Minitor87", event, result, "Dừng đỗ lâu", "LongStop", "_HienTrangHeThong_DungDoLau.png")


    async def Minitor88(self):
        event, result = get_datachecklist("Minitor88")
        await self.list_vehicle.System_status_check("Minitor88", event, result, "Dừng xe nổ máy", "StopAndMachineOn", "_HienTrangHeThong_DungXeNoMay.png")


    async def Minitor89(self):
        event, result = get_datachecklist("Minitor89")
        await self.list_vehicle.System_status_check("Minitor89", event, result, "Khóa đồng hồ", "LockMeter", "_HienTrangHeThong_KhoaDongHo.png")


    async def Minitor90(self):
        event, result = get_datachecklist("Minitor90")
        await self.list_vehicle.System_status_check("Minitor90", event, result, "Mất kết nối đồng hồ", "LostConnectMeter", "_HienTrangHeThong_MatKetNoiDongHo.png")


    async def Minitor91(self):
        event, result = get_datachecklist("Minitor91")
        await self.list_vehicle.System_status_excel("Minitor91", event, result)


    async def Minitor92(self):
        event, result = get_datachecklist("Minitor92")
        await self.list_vehicle.Car_symbol_meaning("Minitor92", event, result)


    async def Minitor93(self):
        event, result = get_datachecklist("Minitor93")
        await self.list_vehicle.Share_vehicle("Minitor93", event, result)


    async def Minitor94(self):
        event, result = get_datachecklist("Minitor94")
        await self.list_vehicle.Share_vehicle_fill_and_coppy("Minitor94", event, result)


    async def Minitor95(self):
        event, result = get_datachecklist("Minitor95")
        await self.list_vehicle.Share_vehicle_minitor("Minitor95", event, result)


    async def Minitor96(self):
        event, result = get_datachecklist("Minitor96")
        await self.list_vehicle.Share_vehicle_route("Minitor96", event, result)


    async def Minitor97(self):
        event, result = get_datachecklist("Minitor97")
        await self.list_vehicle.Check_online_vehicle("Minitor97", event, result)


    async def Minitor98(self):
        event, result = get_datachecklist("Minitor98")
        await self.list_vehicle.Check_countvehicle_web_api("Minitor98", event, result)


    async def Minitor99(self):
        event, result = get_datachecklist("Minitor99")
        await self.list_vehicle.Get_data_check("Minitor99", event, result)


    async def Minitor100(self):
        event, result = get_datachecklist("Minitor100")
        await self.list_vehicle.Get_data_check_address("Minitor100", event, result)


    async def Minitor101(self):
        event, result = get_datachecklist("Minitor101")
        await self.list_vehicle.Get_data_check_not_none("Minitor101", event, result, 2, 5, 2)


    async def Minitor102(self):
        event, result = get_datachecklist("Minitor102")
        await self.list_vehicle.Get_data_check_seat("Minitor102", event, result)


    async def Minitor103(self):
        event, result = get_datachecklist("Minitor103")
        await self.list_vehicle.Get_data_check_time("Minitor103", event, result)


    async def Minitor104(self):
        event, result = get_datachecklist("Minitor104")
        await self.list_vehicle.Get_data_check_can_none("Minitor104", event, result, 2, 7, 2)


    async def Minitor105(self):
        event, result = get_datachecklist("Minitor105")
        await self.list_vehicle.Get_data_check_can_none("Minitor105", event, result, 2, 8, 2)


    async def Minitor106(self):
        event, result = get_datachecklist("Minitor106")
        await self.list_vehicle.Get_data_check_can_none("Minitor106", event, result, 2, 9, 2)


    async def Minitor107(self):
        event, result = get_datachecklist("Minitor107")
        await self.list_vehicle.Get_data_check_v("Minitor107", event, result)



    async def Minitor108(self):
        event, result = get_datachecklist("Minitor108")
        await self.list_vehicle.Get_data_check_not_none("Minitor108", event, result, 2, 11, 2)


    async def Minitor109(self):
        event, result = get_datachecklist("Minitor109")
        await self.list_vehicle.Get_data_check_can_none("Minitor109", event, result, 2, 37, 2)


    async def Minitor110(self):
        event, result = get_datachecklist("Minitor110")
        await self.list_vehicle.Get_data_check_can_none("Minitor110", event, result, 2, 12, 2)


    async def Minitor111(self):
        event, result = get_datachecklist("Minitor111")
        await self.list_vehicle.Get_data_check_not_none("Minitor111", event, result, 2, 13, 2)


    async def Minitor112(self):
        event, result = get_datachecklist("Minitor112")
        await self.list_vehicle.Get_data_check_not_none("Minitor112", event, result, 2, 14, 2)


    async def Minitor113(self):
        event, result = get_datachecklist("Minitor113")
        await self.list_vehicle.Get_data_check_not_none("Minitor113", event, result, 2, 15, 2)


    async def Minitor114(self):
        event, result = get_datachecklist("Minitor114")
        await self.list_vehicle.Get_data_check_not_none("Minitor114", event, result, 2, 16, 2)


    async def Minitor115(self):
        event, result = get_datachecklist("Minitor115")
        await self.list_vehicle.Get_data_check_not_none("Minitor115", event, result, 2, 17, 2)


    async def Minitor116(self):
        event, result = get_datachecklist("Minitor116")
        await self.list_vehicle.Get_data_check_not_none("Minitor116", event, result, 2, 18, 2)


    async def Minitor117(self):
        event, result = get_datachecklist("Minitor117")
        await self.list_vehicle.Get_data_check_not_none("Minitor117", event, result, 2, 19, 2)


    async def Minitor118(self):
        event, result = get_datachecklist("Minitor118")
        await self.list_vehicle.Get_data_check_not_none("Minitor118", event, result, 2, 20, 2)


    async def Minitor119(self):
        event, result = get_datachecklist("Minitor119")
        await self.list_vehicle.Get_data_check_can_none("Minitor119", event, result, 2, 30, 2)


    async def Minitor120(self):
        event, result = get_datachecklist("Minitor120")
        await self.list_vehicle.Get_data_check_can_none("Minitor120", event, result, 2, 31, 2)


    async def Minitor121(self):
        event, result = get_datachecklist("Minitor121")
        await self.list_vehicle.Get_data_check_can_none("Minitor121", event, result, 2, 32, 2)


    async def Minitor122(self):
        event, result = get_datachecklist("Minitor122")
        await self.list_vehicle.Get_data_check_not_none("Minitor122", event, result, 2, 21, 2)


    async def Minitor123(self):
        event, result = get_datachecklist("Minitor123")
        await self.list_vehicle.Get_data_check_not_none("Minitor123", event, result, 2, 22, 2)


    async def Minitor124(self):
        event, result = get_datachecklist("Minitor124")
        await self.list_vehicle.Get_data_check_not_none("Minitor124", event, result, 2, 23, 2)


    async def Minitor125(self):
        event, result = get_datachecklist("Minitor125")
        await self.list_vehicle.Get_data_check_not_none("Minitor125", event, result, 2, 24, 2)


    async def Minitor126(self):
        event, result = get_datachecklist("Minitor126")
        await self.list_vehicle.Get_data_check_not_none("Minitor126", event, result, 2, 25, 2)


    async def Minitor127(self):
        event, result = get_datachecklist("Minitor127")
        await self.list_vehicle.Get_data_check_not_none("Minitor127", event, result, 2, 26, 2)


    async def Minitor128(self):
        event, result = get_datachecklist("Minitor128")
        await self.list_vehicle.Get_data_check_not_none("Minitor128", event, result, 2, 27, 2)


    async def Minitor129(self):
        event, result = get_datachecklist("Minitor129")
        await self.list_vehicle.Get_data_check_not_none("Minitor129", event, result, 2, 28, 2)


    async def Minitor130(self):
        event, result = get_datachecklist("Minitor130")
        await self.list_vehicle.Get_data_check_not_none("Minitor130", event, result, 4, 34, 4)


    async def Minitor131(self):
        event, result = get_datachecklist("Minitor131")
        await self.list_vehicle.Get_data_check_can_none("Minitor131", event, result, 4, 35, 4)


    async def Minitor132(self):
        event, result = get_datachecklist("Minitor132")
        await self.list_vehicle.Get_data_check_not_none("Minitor132", event, result, 4, 36, 4)


    async def Minitor133(self):
        event, result = get_datachecklist("Minitor133")
        await self.list_vehicle.Get_data_check_status("Minitor133", event, result)


    async def Minitor134(self):
        event, result = get_datachecklist("Minitor134")
        await self.list_vehicle.Share_vehicle2("Minitor134", event, result)


    async def Minitor135(self):
        event, result = get_datachecklist("Minitor135")
        await self.list_vehicle.Review_the_route("Minitor135", event, result)


    async def Minitor136(self):
        event, result = get_datachecklist("Minitor136")
        await self.list_vehicle.Share_vehicle_route_8h_quickly("Minitor136", event, result)


    async def Minitor137(self):
        event, result = get_datachecklist("Minitor137")
        await self.list_vehicle.Share_vehicle_route_tab("Minitor137", event, result, var_gpstaxi.see_detail_newtab,
                                                        var_gpstaxi.speed, " Tốc độ : ", "_XemLaiLoTrinh_8hGanDay_XemChiTietTrenCuaSoMoi")

    async def Minitor138(self):
        event, result = get_datachecklist("Minitor138")
        await self.list_vehicle.Share_vehicle_route_tab("Minitor138", event, result, var_gpstaxi.route_inday_button,
                                                        var_gpstaxi.speed, " Tốc độ : ", "_XemLaiLoTrinh_TrongNgay")

    async def Minitor139(self):
        event, result = get_datachecklist("Minitor139")
        await self.list_vehicle.Share_vehicle_route_tab("Minitor139", event, result, var_gpstaxi.route_setting_button,
                                                        var_gpstaxi.speed, " Tốc độ : ", "_XemLaiLoTrinh_TuyChon")

    async def Minitor140(self):
        event, result = get_datachecklist("Minitor140")
        await self.list_vehicle.Status2("Minitor140", event, result)


    async def Minitor141(self):
        event, result = get_datachecklist("Minitor141")
        await self.list_vehicle.Info_devices("Minitor141", event, result)


    async def Minitor142(self):
        event, result = get_datachecklist("Minitor142")
        await self.list_vehicle.Info_devices_check_info("Minitor142", event, result,
                                                        var_gpstaxi.tdDeviceInfo_imei, "_ThongTinThietBi_imei.png")

    async def Minitor143(self):
        event, result = get_datachecklist("Minitor143")
        await self.list_vehicle.Info_devices_check_info("Minitor143", event, result,
                                                        var_gpstaxi.tdDeviceInfo_number, "_ThongTinThietBi_SoHieuXe.png")

    async def Minitor144(self):
        event, result = get_datachecklist("Minitor144")
        await self.list_vehicle.Info_devices_check_info("Minitor144", event, result,
                                                        var_gpstaxi.tdDeviceInfo_liscense_plate, "_ThongTinThietBi_BienSoXe.png")

    async def Minitor145(self):
        event, result = get_datachecklist("Minitor145")
        await self.list_vehicle.Info_devices_check_info("Minitor145", event, result,
                                                        var_gpstaxi.tdDeviceInfo_vin, "_ThongTinThietBi_Vin.png")

    async def Minitor146(self):
        event, result = get_datachecklist("Minitor146")
        await self.list_vehicle.Info_devices_check_info("Minitor146", event, result,
                                                        var_gpstaxi.tdDeviceInfo_time_frist, "_ThongTinThietBi_ThoiDiemHoatDongLanDau.png")

    async def Minitor147(self):
        event, result = get_datachecklist("Minitor147")
        await self.list_vehicle.Info_devices_check_info("Minitor147", event, result,
                                                        var_gpstaxi.tdDeviceInfo_time_curent, "_ThongTinThietBi_ThoiDiemGuiTinGanNhat.png")

    async def Minitor148(self):
        event, result = get_datachecklist("Minitor148")
        await self.list_vehicle.Info_devices_check_info("Minitor148", event, result,
                                                        var_gpstaxi.tdDeviceInfo_gps, "_ThongTinThietBi_ThongTinGPS.png")

    async def Minitor149(self):
        event, result = get_datachecklist("Minitor149")
        await self.list_vehicle.Info_devices_check_info("Minitor149", event, result,
                                                        var_gpstaxi.tdDeviceInfo_phone, "_ThongTinThietBi_DienThoai.png")

    async def Minitor150(self):
        event, result = get_datachecklist("Minitor150")
        await self.list_vehicle.Info_devices_check_info("Minitor150", event, result,
                                                        var_gpstaxi.tdDeviceInfo_type_phone, "_ThongTinThietBi_LoaiThueBao.png")

    async def Minitor151(self):
        event, result = get_datachecklist("Minitor151")
        await self.list_vehicle.Info_devices_check_info("Minitor151", event, result,
                                                        var_gpstaxi.tdDeviceInfo_battery, "_ThongTinThietBi_MucAcQuy.png")

    async def Minitor152(self):
        event, result = get_datachecklist("Minitor152")
        await self.list_vehicle.Info_devices_check_info("Minitor152", event, result,
                                                        var_gpstaxi.tdDeviceInfo_power, "_ThongTinThietBi_Nguon.png")

    async def Minitor153(self):
        event, result = get_datachecklist("Minitor153")
        await self.list_vehicle.Info_devices_check_info("Minitor153", event, result,
                                                        var_gpstaxi.tdDeviceInfo_card, "_ThongTinThietBi_TheNho.png")

    async def Minitor154(self):
        event, result = get_datachecklist("Minitor154")
        await self.list_vehicle.Minitor_camera("Minitor154", event, result)


    async def Minitor155(self):
        event, result = get_datachecklist("Minitor155")
        await self.list_vehicle.See_image_camera("Minitor155", event, result)


    async def Minitor156(self):
        event, result = get_datachecklist("Minitor156")
        await self.list_vehicle.Subscriber_route("Minitor156", event, result)


    async def Minitor157(self):
        event, result = get_datachecklist("Minitor157")
        await self.list_vehicle.Subscriber_route_fill("Minitor157", event, result)


    async def Minitor158(self):
        event, result = get_datachecklist("Minitor158")
        await self.list_vehicle.Subscriber_route_check("Minitor158", event, result, var_gpstaxi.btnSubmit,
                                                       "Lưu", "_NhapThueBaoTuyen_Luu.png")


    async def Minitor159(self):
        event, result = get_datachecklist("Minitor159")
        await self.list_vehicle.Subscriber_route_check("Minitor159", event, result, var_gpstaxi.btnSubmitAndCreateNew,
                                                       "Lưu và tạo mới", "_NhapThueBaoTuyen_LuuVaTaoMoi.png")


    async def Minitor160(self):
        event, result = get_datachecklist("Minitor160")
        await self.list_vehicle.Subscriber_route_check("Minitor160", event, result, var_gpstaxi.btnSubmitAndRedirectTripCost,
                                                       "Lưu và sang trang Bảng giá cước thuê bao tuyến",
                                                       "_NhapThueBaoTuyen_LuuVaSangTrangBangGiaCuocThueBaoTuyen.png")

    async def Minitor161(self):
        event, result = get_datachecklist("Minitor161")
        await self.list_vehicle.Subscriber_route_cancel("Minitor161", event, result)


    async def Minitor162(self):
        event, result = get_datachecklist("Minitor162")
        await self.list_vehicle.Driver_call("Minitor162", event, result)


    async def Minitor163(self):
        event, result = get_datachecklist("Minitor163")
        await self.list_vehicle.Driver_call_button("Minitor163", event, result, var_gpstaxi.Driver_call1_button, "_GiamSat_LaiXeBao_BaoNghi")


    async def Minitor164(self):
        event, result = get_datachecklist("Minitor164")
        await self.list_vehicle.Driver_call_button("Minitor164", event, result, var_gpstaxi.Driver_call2_button, "_GiamSat_LaiXeBao_XeHoatDongLai")


    async def Minitor165(self):
        event, result = get_datachecklist("Minitor165")
        await self.list_vehicle.Hide_vehicle("Minitor165", event, result)


    async def Minitor166(self):
        event, result = get_datachecklist("Minitor166")
        await self.list_vehicle.Route("Minitor166", event, result)


    async def Minitor167(self):
        event, result = get_datachecklist("Minitor167")
        await self.map.Search_curent_vehicle("Minitor167", event, result)


    async def Minitor168(self):
        event, result = get_datachecklist("Minitor168")
        await self.map.Search_curent_vehicle_button("Minitor168", event, result,
                                                    var_gpstaxi.ddlSortCarNearest_listbox2, "_TimXeGanNhat_DoanhThuTrongNgay.png")

    async def Minitor169(self):
        event, result = get_datachecklist("Minitor169")
        await self.map.Search_curent_vehicle_button("Minitor169", event, result,
                                                    var_gpstaxi.ddlSortCarNearest_listbox1, "_TimXeGanNhat_KhoangCach.png")

    async def Minitor170(self):
        event, result = get_datachecklist("Minitor170")
        await self.map.Find_forgotten_items("Minitor170", event, result)


    async def Minitor171(self):
        event, result = get_datachecklist("Minitor171")
        await self.map.Find_forgotten_items_search("Minitor171", event, result)


    async def Minitor172(self):
        event, result = get_datachecklist("Minitor172")
        await self.map.List_driver_not_login("Minitor172", event, result)


    async def Minitor173(self):
        event, result = get_datachecklist("Minitor173")
        await self.map.List_driver_not_login_group("Minitor173", event, result)


    async def Minitor174(self):
        event, result = get_datachecklist("Minitor174")
        await self.map.List_driver_not_login_number("Minitor174", event, result)


    async def Minitor175(self):
        event, result = get_datachecklist("Minitor175")
        await self.map.List_driver_not_login_update_data("Minitor175", event, result)


    async def Minitor176(self):
        event, result = get_datachecklist("Minitor176")
        await self.map.List_driver_not_login_excel("Minitor176", event, result)


    async def Minitor177(self):
        event, result = get_datachecklist("Minitor177")
        await self.map.Add_a_marker("Minitor177", event, result)


    async def Minitor178(self):
        event, result = get_datachecklist("Minitor178")
        await self.map.Add_a_marker_save("Minitor178", event, result)


    async def Minitor179(self):
        event, result = get_datachecklist("Minitor179")
        await self.map.Add_a_marker_update("Minitor179", event, result)


    async def Minitor180(self):
        event, result = get_datachecklist("Minitor180")
        await self.map.Add_a_marker_delete("Minitor180", event, result)


    async def Minitor181(self):
        event, result = get_datachecklist("Minitor181")
        await self.map.See_address("Minitor181", event, result)


    async def Minitor182(self):
        event, result = get_datachecklist("Minitor182")
        await self.map.Measure_distance1("Minitor182", event, result)


    async def Minitor183(self):
        event, result = get_datachecklist("Minitor183")
        await self.map.Navigation("Minitor183", event, result)


    async def Minitor184(self):
        event, result = get_datachecklist("Minitor184")
        await self.map.Garage_vehicles("Minitor184", event, result)


    async def Minitor185(self):
        event, result = get_datachecklist("Minitor185")
        await self.map.Garage_vehicles_checkinfo("Minitor185", event, result)


    async def Minitor186(self):
        event, result = get_datachecklist("Minitor186")
        await self.map.Find_vehicles_stop("Minitor186", event, result)


    async def Minitor187(self):
        event, result = get_datachecklist("Minitor187")
        await self.map.Find_vehicles_stop_checkbox("Minitor187", event, result, "No", "_TimXeDungDoTrongVungDH_KhongTichChon.png")


    async def Minitor188(self):
        event, result = get_datachecklist("Minitor188")
        await self.map.Find_vehicles_stop_checkbox("Minitor188", event, result, "Yes", "_TimXeDungDoTrongVungDH_TichChon.png")


    async def Minitor189(self):
        event, result = get_datachecklist("Minitor189")
        await self.map.Find_vehicles_in_the_zone("Minitor189", event, result)


    async def Minitor190(self):
        event, result = get_datachecklist("Minitor190")
        await self.map.Find_vehicles_in_the_zone_checkinfo("Minitor190", event, result)


    async def Minitor191(self):
        event, result = get_datachecklist("Minitor191")
        await self.map.Toggle_point_zones("Minitor191", event, result)


    async def Minitor192(self):
        event, result = get_datachecklist("Minitor192")
        await self.map.Toggle_point_zones_checkbox("Minitor192", event, result, "No", "_AnHienVungDiem_TatHienThi.png")


    async def Minitor193(self):
        event, result = get_datachecklist("Minitor193")
        await self.map.Toggle_point_zones_checkbox("Minitor193", event, result, "Yes", "_AnHienVungDiem_BatHienThi.png")


    async def Minitor194(self):
        event, result = get_datachecklist("Minitor194")
        await self.map.Show_hide_boundary("Minitor194", event, result)


    async def Minitor195(self):
        event, result = get_datachecklist("Minitor195")
        await self.map.Startup_configuration("Minitor195", event, result)


    async def Minitor196(self):
        event, result = get_datachecklist("Minitor196")
        await self.map.Startup_configuration_type("Minitor196", event, result, "Bình Anh", "_CauHinhKhoiDong_BinhAnh.png")


    async def Minitor197(self):
        event, result = get_datachecklist("Minitor197")
        await self.map.Startup_configuration_type("Minitor197", event, result, "Vệ tinh", "_CauHinhKhoiDong_VeTinh.png")


    async def Minitor198(self):
        event, result = get_datachecklist("Minitor198")
        await self.map.Startup_configuration_type("Minitor198", event, result, "Bản đồ", "_CauHinhKhoiDong_BanDo.png")


    async def Minitor199(self):
        event, result = get_datachecklist("Minitor199")
        await self.multiple_vehicles.Monitor_multiple_vehicles("Minitor199", event, result)


    async def Minitor200(self):
        event, result = get_datachecklist("Minitor200")
        await self.multiple_vehicles.Monitor_3_vehicles("Minitor200", event, result)


    async def Minitor201(self):
        event, result = get_datachecklist("Minitor201")
        await self.multiple_vehicles.Monitor_1_vehicles("Minitor201", event, result)


    async def Minitor202(self):
        event, result = get_datachecklist("Minitor202")
        await self.multiple_vehicles.Zoom_in("Minitor202", event, result)


    async def Minitor203(self):
        event, result = get_datachecklist("Minitor203")
        await self.multiple_vehicles.Close("Minitor203", event, result)


    async def Minitor204(self):
        event, result = get_datachecklist("Minitor204")
        await self.multiple_vehicles.Number_LiscensePlate("Minitor204", event, result)


    async def Minitor205(self):
        event, result = get_datachecklist("Minitor205")
        await self.multiple_vehicles.Check_info_status_path("Minitor205", event, result, 1,
                                                       var_gpstaxi.status_location, "_GiamSatNhieuXe_ViTri.png")

    async def Minitor206(self):
        event, result = get_datachecklist("Minitor206")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor206", event, result,
                                                                 "Loại xe", "_GiamSatNhieuXe_LoaiXe.png")

    async def Minitor207(self):
        event, result = get_datachecklist("Minitor207")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor207", event, result,
                                                                 "Ngày/Giờ", "_GiamSatNhieuXe_NgayGio.png")

    async def Minitor208(self):
        event, result = get_datachecklist("Minitor208")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor208", event, result,
                                                                 "Lái xe", "_GiamSatNhieuXe_LaiXe.png")

    async def Minitor209(self):
        event, result = get_datachecklist("Minitor209")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor209", event, result,
                                                                 "Điện thoại", "_GiamSatNhieuXe_DienThoai.png")

    async def Minitor210(self):
        event, result = get_datachecklist("Minitor210")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor210", event, result,
                                                                 "Vận tốc GPS/Cơ", "_GiamSatNhieuXe_VanTocGPSCo.png")

    async def Minitor211(self):
        event, result = get_datachecklist("Minitor211")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor211", event, result,
                                                                 "Gara", "_GiamSatNhieuXe_Gara.png")

    async def Minitor212(self):
        event, result = get_datachecklist("Minitor212")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor212", event, result,
                                                                 "Điều hòa", "_GiamSatNhieuXe_DieuHoa.png")

    async def Minitor213(self):
        event, result = get_datachecklist("Minitor213")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor213", event, result,
                                                                 "Máy", "_GiamSatNhieuXe_May.png")

    async def Minitor214(self):
        event, result = get_datachecklist("Minitor214")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor214", event, result,
                                                                 "Trạng thái", "_GiamSatNhieuXe_TrangThai.png")

    async def Minitor215(self):
        event, result = get_datachecklist("Minitor215")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor215", event, result,
                                                                 "Nhóm đội", "_GiamSatNhieuXe_NhomDoi.png")

    async def Minitor216(self):
        event, result = get_datachecklist("Minitor216")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor216", event, result,
                                                                 "Loại đồng hồ", "_GiamSatNhieuXe_LoaiDongHo.png")

    async def Minitor217(self):
        event, result = get_datachecklist("Minitor217")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor217", event, result,
                                                                 "KM CK/Rỗng", "_GiamSatNhieuXe_KmRong.png")

    async def Minitor218(self):
        event, result = get_datachecklist("Minitor218")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor218", event, result,
                                                                 "Tổng CK", "_GiamSatNhieuXe_TongCK.png")

    async def Minitor219(self):
        event, result = get_datachecklist("Minitor219")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor219", event, result,
                                                                 "Tổng doanh thu", "_GiamSatNhieuXe_TongDoanhThu.png")

    async def Minitor220(self):
        event, result = get_datachecklist("Minitor220")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor220", event, result,
                                                                 "Tiền CK hiện tại", "_GiamSatNhieuXe_TongCKHienTai.png")

    async def Minitor221(self):
        event, result = get_datachecklist("Minitor221")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor221", event, result,
                                                                 "Thời gian chờ", "_GiamSatNhieuXe_ThoiGianCho.png")

    async def Minitor222(self):
        event, result = get_datachecklist("Minitor222")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor222", event, result,
                                                                 "KM CK đang chạy", "_GiamSatNhieuXe_KMCKDangChay.png")

    async def Minitor223(self):
        event, result = get_datachecklist("Minitor223")
        await self.multiple_vehicles.Check_info_status_tab1_name("Minitor223", event, result,
                                                                 "Thông tin phí:", "_GiamSatNhieuXe_ThongTinPhi.png")

    async def Minitor224(self):
        event, result = get_datachecklist("Minitor224")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor224", event, result,
                                                                 "Số VIN", "_GiamSatNhieuXe_SoVin.png")

    async def Minitor225(self):
        event, result = get_datachecklist("Minitor225")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor225", event, result,
                                                                 "Lái xe", "_GiamSatNhieuXe_LaiXe.png")

    async def Minitor226(self):
        event, result = get_datachecklist("Minitor226")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor226", event, result,
                                                                 "Giấy phép lái xe", "_GiamSatNhieuXe_GiayPhepLaiXe.png")

    async def Minitor227(self):
        event, result = get_datachecklist("Minitor227")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor227", event, result,
                                                                 "Quá tốc độ", "_GiamSatNhieuXe_QuaTocDo.png")

    async def Minitor228(self):
        event, result = get_datachecklist("Minitor228")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor228", event, result,
                                                                 "TG LX liên tục", "_GiamSatNhieuXe_ThoiGianLaiXeLienTuc.png")

    async def Minitor229(self):
        event, result = get_datachecklist("Minitor229")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor229", event, result,
                                                                 "TG LX trong ngày", "_GiamSatNhieuXe_ThoiGianLaiXeTrongNgay.png")

    async def Minitor230(self):
        event, result = get_datachecklist("Minitor230")
        await self.multiple_vehicles.Check_info_status_tab2_name("Minitor230", event, result,
                                                                 "Sở quản lý", "_GiamSatNhieuXe_SoQuanLy.png")


    async def Route01(self):
        event, result = get_datachecklist("Route01")
        await self.route.Route("Route01", event, result)


    async def Route02(self):
        event, result = get_datachecklist("Route02")
        await self.route.Get_data("Route02", event, result)


    async def Route03(self):
        event, result = get_datachecklist("Route03")
        await self.route.Icon_config("Route03", event, result)


    async def Route04(self):
        event, result = get_datachecklist("Route04")
        await self.route.Config_text("Route04", event, result,
                                     "Hiển thị mắt thần", "_LoTrinh_CauHinh_HienThiMatThan")

    async def Route05(self):
        event, result = get_datachecklist("Route05")
        await self.route.Config_text("Route05", event, result,
                                     "Gộp dừng đỗ", "_LoTrinh_CauHinh_GopDungDo")

    async def Route06(self):
        event, result = get_datachecklist("Route06")
        await self.route.Config_checkbox("Route06", event, result, var_gpstaxi.chkDisplaySpdMeter,
                                     "V cơ", "_LoTrinh_CauHinh_VCo")

    async def Route07(self):
        event, result = get_datachecklist("Route07")
        await self.route.Config_checkbox("Route07", event, result, var_gpstaxi.chkDisplayKm,
                                     "Km", "_LoTrinh_CauHinh_Km")

    async def Route08(self):
        event, result = get_datachecklist("Route08")
        await self.route.Config_checkbox("Route08", event, result, var_gpstaxi.chkDisplayEngineSts,
                                     "Máy", "_LoTrinh_CauHinh_May")

    async def Route09(self):
        event, result = get_datachecklist("Route09")
        await self.route.Config_checkbox("Route09", event, result, var_gpstaxi.chkDisplayAcSts,
                                     "Điều hòa", "_LoTrinh_CauHinh_DieuHoa")

    async def Route10(self):
        event, result = get_datachecklist("Route10")
        await self.route.Config_checkbox("Route10", event, result, var_gpstaxi.chkDisplayLatLong,
                                     "Kinh độ, vĩ độ", "_LoTrinh_CauHinh_KinhDoViDo")

    async def Route11(self):
        event, result = get_datachecklist("Route11")
        await self.route.Config_checkbox("Route11", event, result, var_gpstaxi.chkDisplayVBGT,
                                     "VBGT", "_LoTrinh_CauHinh_VBGT")

    async def Route12(self):
        event, result = get_datachecklist("Route12")
        await self.route.Config_text1("Route12", event, result, "chkDisplayCustomer",
                                      "Hiển thị Địa điểm đón trả khách", "_LoTrinh_CauHinh_HienThiDiaDiemDonTraKhach")

    async def Route13(self):
        event, result = get_datachecklist("Route13")
        await self.route.Config_text1("Route13", event, result, "chkDisplayLndMark",
                                      "Hiển thị Điểm, vùng", "_LoTrinh_CauHinh_HienThiDiemVung")

    async def Route14(self):
        event, result = get_datachecklist("Route14")
        await self.route.Config_checkbox("Route14", event, result, var_gpstaxi.chkDisplayTemperature,
                                     "Nhiệt độ", "_LoTrinh_CauHinh_VBGT")

    async def Route15(self):
        event, result = get_datachecklist("Route15")
        await self.route.Config_defaul("Route15", event, result, "Thời gian", "_LoTrinh_Popup_ThoiGian")

    async def Route16(self):
        event, result = get_datachecklist("Route16")
        await self.route.Config_defaul("Route16", event, result, "V GPS", "_LoTrinh_Popup_VGPS")


    async def Route17(self):
        event, result = get_datachecklist("Route17")
        await self.route.Icon_help("Route17", event, result)


    async def Route18(self):
        event, result = get_datachecklist("Route18")
        await self.route.Check_icon("Route18", event, result, var_gpstaxi.btnPlay, "_LoTrinh_IconRun")


    async def Route19(self):
        event, result = get_datachecklist("Route19")
        await self.route.Check_icon("Route19", event, result, var_gpstaxi.btnStop, "_LoTrinh_IconDung")


    async def Route20(self):
        event, result = get_datachecklist("Route20")
        await self.route.Check_icon("Route20", event, result, var_gpstaxi.btnDecSpeed, "_LoTrinh_GiamToc")


    async def Route21(self):
        event, result = get_datachecklist("Route21")
        await self.route.Check_icon("Route21", event, result, var_gpstaxi.btnIncSpeed, "_LoTrinh_TangToc")


    async def Route22(self):
        event, result = get_datachecklist("Route22")
        await self.route.Check_icon("Route22", event, result, var_gpstaxi.btnFastForward, "_LoTrinh_TocDoToiDa")


    async def Route23(self):
        event, result = get_datachecklist("Route23")
        await self.route.Icon_print("Route23", event, result)


    async def Route24(self):
        event, result = get_datachecklist("Route24")
        await self.route.Icon_excel("Route24", event, result)


    async def Report01(self):
        event, result = get_datachecklist("Report01")
        await self.report.Detailed_trip_report_by_vehicle("Report01", event, result)


    async def Report02(self):
        event, result = get_datachecklist("Report02")
        await self.report.Detailed_trip_report_by_vehicle_search("Report02", event, result)


    async def Report03(self):
        event, result = get_datachecklist("Report03")
        await self.report.Detailed_trip_report_by_vehicle_report("Report03", event, result)


    async def Report04(self):
        event, result = get_datachecklist("Report04")
        await self.report.Detailed_trip_report_by_vehicle_excel("Report04", event, result)


    async def Report05(self):
        event, result = get_datachecklist("Report05")
        await self.report.Summary_trip_report_by_vehicle("Report05", event, result)


    async def Report06(self):
        event, result = get_datachecklist("Report06")
        await self.report.Summary_trip_report_by_vehicle_search("Report06", event, result)


    async def Report07(self):
        event, result = get_datachecklist("Report07")
        await self.report.Summary_trip_report_by_vehicle_report("Report07", event, result)


    async def Report08(self):
        event, result = get_datachecklist("Report08")
        await self.report.Summary_trip_report_by_vehicle_excel("Report08", event, result)


    async def Report09(self):
        event, result = get_datachecklist("Report09")
        await self.report.Speeding_report("Report09", event, result)


    async def Report10(self):
        event, result = get_datachecklist("Report10")
        await self.report.Speeding_report_search("Report10", event, result)


    async def Report11(self):
        event, result = get_datachecklist("Report11")
        await self.report.Speeding_report_excel("Report11", event, result)





























