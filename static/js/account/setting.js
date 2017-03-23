/**
 * Created by allen on 16/9/7.
 */
require(["jquery", "bsAlert", "csrfToken", "validator"], function ($, bsAlert, csrfTokenHeader) {
    $('form').validator().on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
            var phone = $("#phone").val();
            var sign = $("#sign").val();
            $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/account/settings/",
                data: {
                    phone_number: phone,
                    sign: sign
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                        bsAlert("修改成功");
                    }
                    else{
                        bsAlert(data.data);
                    }
                },
                error: function () {
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }

            });
            return false;
        }
    });
});


