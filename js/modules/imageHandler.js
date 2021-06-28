const { loadImage } = require('canvas');

// Pass this from the root dir
const image_dir = './res/image_refs/'
// testing
process.chdir('..');
process.chdir('..');
const image_list = {
    "reports_window": image_dir + "reports_window.png",
    "ico_root": image_dir + "root_test.png",
    "ico_root_t": image_dir + "root.png",
    "departures": image_dir + "departure_all.png",
    "cashier_login_window": image_dir + "cashier_login_window.png",
    "field_reports": image_dir + "report_bar.png",
    "finpayments": image_dir + "finpayments.png",
    "finjrnlbytrans": image_dir + "finjrnlbytrans.png",
    "first_open": image_dir + "first_open.png",
    // banner
    "misc": image_dir + "banner/misc_banner.png",
    "reports": image_dir + "banner/reports_banner.png",
    "menu_misc": image_dir + "banner/misc_menu.png",
    "cashier": image_dir + "banner/cashiering_banner.png",
    "func": image_dir + "banner/shift_functions.png",
    "batch": image_dir + "banner/batch_folios_banner.png",
    // common
    "btn_search": image_dir + "common/search.png",
    "btn_yes": image_dir + "common/yes.png",
    "btn_print": image_dir + "common/print.png",
    "btn_close": image_dir + "common/close.png",
    "btn_exit": image_dir + "common/exit.png",
    "btn_login": image_dir + "common/login.png",
    "btn_next": image_dir + "common/next.png",
    "login": image_dir + "common/password_box.png",
    "login_a": image_dir + "common/password_box_a.png",
    // folio
    "a_bill": image_dir + "folio/advance_bill.png",
    "a_guest": image_dir + "folio/all_guest.png",
    "a_windows": image_dir + "folio/all_windows.png",
    "c_cards": image_dir + "folio/credit_card.png",
    "depart": image_dir + "folio/depart_tomorrow.png",
    "r_order": image_dir + "folio/room_order.png",
    "sim": image_dir + "folio/simulate.png",
};


function InitImageMap(){
  for(var imageName in image_list){
    image_list[imageName] = loadImage(image_list[imageName]);
    //image_list.set(imageName,loadImage(image_list[imageName]));
  }
}

InitImageMap();
// So we got the images all loaded, that's the easy part.
function capture_screen(){
  var pic = robot.screen.capture();
}


function search_screen(SearchObject){
  // I need to find an equivelant of 'pyautogui.locateOnScreen' but for jscript
}

search_screen('login');
