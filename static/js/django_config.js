/**
 * Created by allen on 16/8/26.
 */
var require = {
    urlArgs: "v=2.1",
    // RequireJS 通过一个相对的路径 baseUrl来加载所有代码。baseUrl通常被设置成data-main属性指定脚本的同级目录。
    baseUrl: "/static/js/",
    paths: {
        jquery: "lib/jquery/jquery.min",
        validator: "lib/validator/validator",

        bsAlert: "utils/bsAlert",
        csrfToken: "utils/csrfToken",
        uploader: "utils/uploader",
        web_uploader: "utils/web_uploader",

        imagezoom: "lib/ui/imagezoom",
        memenu: "lib/ui/memenu",
        responseiveslides: "lib/ui/responsiveslides.min",
        simpleCart : "lib/ui/simpleCart.min",
        do_some: "lib/ui/do_some",

        // bootstrap组件
        modal: "lib/bootstrap/modal",
        dropdown: "lib/bootstrap/dropdown",
        transition: "lib/bootstrap/transition",
        collapse: "lib/bootstrap/collapse",

        bootstrap: "lib/bootstrap/bootstrap",

        register: "account/register",
        account_setting: "account/setting",
        account_avatar_setting: "account/avatar",
        reset_pwd: "account/reset_pwd",
        login: "account/login",
        logout: "account/logout",
        apply_reset_pwd: "account/apply_reset_pwd",

        //address
        commonobj: "address/commonobj",
        swiper: "address/swiper",
        zone: "address/zone",
        generate_addr: "address/generate_addr",
        add_address: "address/add_address",

        //store
        buy_item: "store/buy_item",
        cart: "store/cart",
        angular: "lib/angular/angular",
    },
};