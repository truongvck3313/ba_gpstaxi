import logging
import asyncio
import time

from retry import retry
from playwright.async_api import Page
import module_other_gpstaxi
import var_gpstaxi



logging.basicConfig(
    handlers=[logging.FileHandler(filename=var_gpstaxi.logpath, encoding='utf-8', mode='a+')],
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%F %A %T",
    level=logging.INFO
)


class Login:
    def __init__(self, page: Page):
        self.page = page


    @retry(tries=2, delay=2, backoff=1, jitter=5)
    async def login_gpstaxi(self, user, password):
        """Hàm login chuẩn"""
        if not await self.goto_linktest():
            return

        await self.page.fill(f"xpath={var_gpstaxi.login_user}", user)
        await self.page.fill(f"xpath={var_gpstaxi.login_password}", password)
        await self.page.click(f"xpath={var_gpstaxi.button_login}")

        await self.page.wait_for_selector(f"xpath={var_gpstaxi.minitor}", timeout=15000)
        # time.sleep(5)

        if user != var_gpstaxi.data['login']['binhanh_tk']:
            try:
                await self.page.click(f"xpath={var_gpstaxi.icon_refresh}", timeout=22000)
                await Login.delete_notication(self)
            except:
                await Login.delete_notication(self)



    @retry(tries=2, delay=2, backoff=1, jitter=5)
    async def goto(self, type_goto, data_goto, check_goto):
        await self.login_gpstaxi(var_gpstaxi.data['login']['binhanh_tk'],
                                 var_gpstaxi.data['login']['binhanh_mk'])

        if type_goto == "Mã XN":
            await self.page.click(f"xpath={var_gpstaxi.radGotoByXNCode}")

        if type_goto == "Người dùng":
            await self.page.click(f"xpath={var_gpstaxi.radGotoByUsername}")


        await self.page.fill(f"xpath={var_gpstaxi.txtXNCodeGoto}", data_goto)
        await asyncio.sleep(0.5)

        await self.page.evaluate("""(xpath) => {
            document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
                    .singleNodeValue.click();
        }""", var_gpstaxi.btnGotoCompany)

        await self.page.wait_for_selector(f"xpath=//*[contains(text(), '{check_goto}')]", timeout=10000)
        print("n2")
        try:
            await self.page.click(f"xpath={var_gpstaxi.icon_refresh}", timeout=10000)
            await Login.delete_notication(self)
        except:
            await Login.delete_notication(self)






    async def goto_linktest(self):
        """Đi tới linktest với xử lý ERR_ABORTED"""
        try:
            await self.page.context.clear_cookies()
        except Exception:
            pass

        try:
            await self.page.goto(var_gpstaxi.linktest, timeout=60000, wait_until="domcontentloaded")
            return True
        except Exception as e:
            if "net::ERR_ABORTED" in str(e):
                logging.warning(f"Page.goto bị ERR_ABORTED nhưng bỏ qua: {e}")
                return True
            logging.error(f"Không thể truy cập {var_gpstaxi.linktest}: {e}")
            return False


    async def check_login(self, code, event, result, type_minitor, user, password, pathcheck, desire, name_image):
        """Check quyền tài khoản"""
        if not await self.goto_linktest():
            return

        await self.page.fill(f"xpath={var_gpstaxi.login_user}", user)
        await self.page.fill(f"xpath={var_gpstaxi.login_password}", password)
        await self.page.click(f"xpath={var_gpstaxi.button_login}")

        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.minitor}", timeout=10000)
            logging.info("Đăng nhập thành công, chuyển hướng trang.")
        except Exception as e:
            logging.error(f"Đăng nhập thất bại hoặc không chuyển hướng được: {e}")

        # Chọn loại kiểm tra
        if type_minitor == 2:
            await module_other_gpstaxi.write_result_text_inner_text_other(
                self.page, code, event, result,
                "Đăng nhập - Check quyền tài khoản",
                pathcheck, desire, name_image
            )
        elif type_minitor == 1:
            await module_other_gpstaxi.write_result_text_inner_text(
                self.page, code, event, result,
                "Đăng nhập - Check quyền tài khoản",
                pathcheck, desire, name_image
            )
        elif type_minitor == 0:
            await module_other_gpstaxi.write_result_not_displayed(
                self.page, code, event, result,
                "Đăng nhập - Check quyền tài khoản",
                pathcheck, name_image
            )


    async def wrong_login(self, code, event, result):
        """Login sai mật khẩu"""
        if not await self.goto_linktest():
            return

        await self.page.fill(f"xpath={var_gpstaxi.login_user}", var_gpstaxi.data['login']['binhanh_tk'])
        await self.page.fill(f"xpath={var_gpstaxi.login_password}", "11111")
        await self.page.click(f"xpath={var_gpstaxi.button_login}")
        await asyncio.sleep(2.3)

        await module_other_gpstaxi.write_result_text_inner_text(
            self.page, code, event, result,
            "Đăng nhập - Đăng nhập với tài khoản đúng, mật khẩu sai",
            var_gpstaxi.login_error,
            "Tài khoản hoặc mật khẩu không hợp lệ. Vui lòng đăng nhập lại hoặc liên hệ tới quản trị để được trợ giúp",
            "_DangNhap_TaiKhoanDungMatKhauSai.png"
        )


    async def forgot_password(self, code, event, result):
        """Quên mật khẩu"""
        if not await self.goto_linktest():
            return

        await self.page.click(f"xpath={var_gpstaxi.forgot_password}")
        await self.page.fill(f"xpath={var_gpstaxi.forgot_user}", var_gpstaxi.data['login']['quenmatkhau_tk'])
        await self.page.fill(f"xpath={var_gpstaxi.forgot_phone}", var_gpstaxi.data['login']['sodienthoai_mk'])
        await self.page.click(f"xpath={var_gpstaxi.send_verification_code}")
        await asyncio.sleep(2)

        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.check_forgot_password1}", timeout=500)
            await module_other_gpstaxi.write_result_text_inner_text(
                self.page, code, event, result,
                "Đăng nhập - Quên mật khẩu",
                var_gpstaxi.check_forgot_password1, "Mã OTP xác minh: *", "_QuenMatKhau.png"
            )
        except:
            await module_other_gpstaxi.write_result_text_inner_text(
                self.page, code, event, result,
                "Đăng nhập - Quên mật khẩu",
                var_gpstaxi.check_forgot_password2,
                "Mã xác minh được gửi qua zalo của số điện thoại này", "_QuenMatKhau.png"
            )


    async def remember_to_log_in(self, code, event, result, checkbox):
        """Check ghi nhớ đăng nhập"""
        if not await self.goto_linktest():
            return

        await self.page.fill(f"xpath={var_gpstaxi.login_user}", var_gpstaxi.data['login']['binhthuong_tk'])
        await self.page.fill(f"xpath={var_gpstaxi.login_password}", var_gpstaxi.data['login']['binhthuong_mk'])

        if checkbox == True:
            remember_box = self.page.locator(f"xpath={var_gpstaxi.RememberMe}")
            await remember_box.click()
            await asyncio.sleep(1)


        await self.page.click(f"xpath={var_gpstaxi.button_login}")
        await self.page.wait_for_selector(f"xpath={var_gpstaxi.minitor}", timeout=5000)

        await self.page.goto(var_gpstaxi.linktest, timeout=60000, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        if checkbox == True:
            await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result,
                "Đăng nhập - Check quyền tài khoản", var_gpstaxi.minitor, "Giám sát", "_GhiNhoDangNhap_TichChon.png")
        else:
            await module_other_gpstaxi.write_result_text_inner_text(self.page, code, event, result,
                "Đăng nhập - Check quyền tài khoản", var_gpstaxi.forgot_password, "Quên mật khẩu",  "_GhiNhoDangNhap_BoTichChon.png")




    async def delete_notication(self):
        # self.login_page = Login(self.page)
        # await self.login_page.delete_notication()
        try:
            await self.page.click(f"xpath={var_gpstaxi.close}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n0")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.exit}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n1")
            pass

        try:
            await self.page.click(f"xpath={var_gpstaxi.close_missing}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n2")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close1}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n3")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close2}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n4")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close3}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n5")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close4}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n6")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close5}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n7")
            pass

        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close6}", timeout=200)
            await asyncio.sleep(1)
        except:
            print("n8")
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close7}", timeout=200)
            await asyncio.sleep(1)
            print("n9")
        except:
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close8}", timeout=200)
            await asyncio.sleep(1)
            print("n10")
        except:
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close9}", timeout=200)
            await asyncio.sleep(1)
            print("n11")
        except:
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close10}", timeout=200)
            await asyncio.sleep(1)
            print("n12")
        except:
            pass
        try:
            await self.page.click(f"xpath={var_gpstaxi.i_close11}", timeout=200)
            await asyncio.sleep(1)
            print("n13")
        except:
            pass




class Link:
    def __init__(self, page: Page):
        self.page = page

    async def check_link(self, code, event, result, type_link, path_link, pathcheck, desire, name_image):
        # Truy cập link chính
        try:
            await self.page.goto(var_gpstaxi.linktest, timeout=60000, wait_until="load")
        except Exception as e:
            print(f"Không thể truy cập link chính: {e}")
            return

        # Chờ selector login_user
        try:
            await self.page.wait_for_selector(f"xpath={var_gpstaxi.login_user}", timeout=10000)
        except Exception as e:
            print(f"Selector login_user không xuất hiện: {e}")

        # --- type_link = 0: kiểm tra text trong trang ---
        if type_link == 0:
            await module_other_gpstaxi.write_result_text_inner_text(
                self.page, code, event, result,
                "Đăng nhập - Link liên kết", pathcheck, desire, name_image
            )

        # --- type_link = 1: click link và kiểm tra URL ---
        elif type_link == 1:
            await self.page.click(f"xpath={path_link}")
            await asyncio.sleep(3.5)
            await module_other_gpstaxi.write_result_text_url_in(
                self.page, code, event, result,
                "Đăng nhập - Link liên kết", desire, name_image
            )


        # --- type_link = 2: mở link ra tab mới ---
        elif type_link == 2:
            async with self.page.context.expect_page() as new_page_info:
                await self.page.click(f"xpath={path_link}")

            # LẤY TAB MỚI (phải có await)
            new_page = await new_page_info.value

            # Đợi tab mới load
            await new_page.wait_for_load_state("load", timeout=15000)

            # Lấy locator
            locator = new_page.locator(f"xpath={pathcheck}").first
            await locator.wait_for(state="visible", timeout=10000)

            # Lấy text
            check_text = await locator.text_content()
            print(f"{check_text}")


            # Ghi kết quả vào Excel (sync function, không cần await)
            module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 6, check_text)

            if check_text == desire:
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Pass")
            else:
                await new_page.screenshot(path=f"{var_gpstaxi.imagepath}{code}{name_image}.png", full_page=True)
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 7, "Fail")
                module_other_gpstaxi.writeData(var_gpstaxi.checklistpath, "Checklist", code, 13, code + name_image)

            await new_page.close()

