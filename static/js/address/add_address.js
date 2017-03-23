/**
 * Created by allen on 16/9/7.
 */
require(["jquery", "bsAlert", "csrfToken", "validator"], function ($, bsAlert, csrfTokenHeader) {
   function clearAddress(){
        $("#name").val('');
        $("#detail_info").val('');
        $('#email').val('');
        $('#phone_number').val('');
        $('#s1').val('');
        $('#s2').val('');
        $('#s3').val('');
        $('#address_id').val('-1');
   }

   function addAddress(name, detail_address, email, phone_number
   , province, city, region, address_id) {
       var addressliHtml = '<li id=addr-li-' + address_id + '>'+
            '<p><em class="name">' + name + '</em>(<em class="phone">' + phone_number + '</em>)</p>' +
            ' <p class="all-address">' + province + '&nbsp;' + city + '&nbsp;' + region + '&nbsp;' + detail_address + '</p>' +
            '<p><em class="email">'+email+'</em></p>'+
            '<p class="new_line"><br></p>' +
            '<p class="address_action">' +
            '<span><a href="#" class="edit float_none" id=edit-addr-' + address_id  + '><i class="edit_icon"></i>修改</a></span>' +
            '<span><a href="#" class="delete float_none" id=delete-addr-' + address_id  + '><i class="delete_icon"></i>删除</a></span>' +
            '</p>' +
            '</li>';
        $("#addresslist").prepend(addressliHtml);
   }

   function modifyAddress(name, detail_address, email, phone_number
   , province, city, region, address_id) {
        var modidy_li = $('#addr-li-'+address_id);
        modidy_li.find(".name").text(name);
        modidy_li.find(".phone").text(phone_number);
        modidy_li.find(".email").text(email);
        modidy_li.find(".all-address").html(province + '&nbsp;' + city + '&nbsp;' + region + '&nbsp;' + detail_address);
   }

    $('form').validator().on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
            var name = $("#name").val();
            var detail_address = $("#detail_info").val();
            var email = $('#email').val();
            var phone_number = $('#phone_number').val();
            var province = $('#s1').val();
            var city = $('#s2').val();
            var region = $('#s3').val();
            var address_id = $('#address_id').val();
            $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/account/settings/address/",
                data: {
                    name: name,
                    detail_address: detail_address,
                    email: email,
                    phone_number: phone_number,
                    province: province,
                    city: city,
                    region: region,
                    address_id: address_id,
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                        clearAddress();
                        var new_addr_id = data.data.id;
                        if (data.data.is_modify) {
                            bsAlert("修改成功");
                            modifyAddress(name, detail_address, email, phone_number
                            , province, city, region, new_addr_id);
                        }
                        else {
                            bsAlert("添加成功");
                            addAddress(name, detail_address, email, phone_number
                            , province, city, region, new_addr_id);
                        }
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
        else {
            bsAlert("额 没有ajax成功哎!");
        }
    });
    
    $("#addresslist").on("click","a[id^=edit-addr-]", function (event) {
        event.preventDefault();
        var primary_key = $(this).attr('id').split('-')[2];
        var name = $(this).parents("li").find(".name").text();
        var phone=$(this).parents("li").find(".phone").text();
        var allAddress=$(this).parents("li").find(".all-address").html();
        var addressArray=allAddress.split("&nbsp;");
        var s1=addressArray[0];
        var s2=addressArray[1];
        var s3=addressArray[2];
        var addressinfo=addressArray[3];
        var email = $(this).parents("li").find(".email").text();
        $("#name").val(name);
        $("#s1").val(s1);
        $("#s1").trigger("change");
        $("#s2").val(s2);
        $("#s2").trigger("change");
        $("#s3").val(s3);
        $("#detail_info").val(addressinfo);
        $("#phone_number").val(phone);
        $("#email").val(email);
        $('#address_id').val(primary_key);
    });

    $("#addresslist").on("click",".delete", function (event) {
        event.preventDefault();
        var primary_key = $(this).attr('id').split('-')[2];
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/account/settings/address/",
                data: {
                    address_id: primary_key,
                },
                dataType: "json",
                method: "delete",
                success: function (data) {
                    if (!data.code) {
                        bsAlert("删除成功");
                        var li = $('#addr-li-'+data.data);
                        li.hide();
                    }
                    else{
                        bsAlert(data.data);
                    }
                },
                error: function () {
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    });
});