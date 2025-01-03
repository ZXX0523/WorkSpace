document.addEventListener('DOMContentLoaded', function() {

});
    document.addEventListener('DOMContentLoaded', function() { // 确保DOM加载完毕
//            当切换点击环境/套餐期长/画具时，调接口查询套餐信息
            var radios = document.getElementsByName('PaintingTools'); // 获取所有name为exampleRadio的radio按钮
            for(var i = 0; i < radios.length; i++) {
                radios[i].addEventListener('change', function(event) { // 为每个按钮添加change事件监听
                    if(this.checked) { // 确保只有被选中的按钮会触发
                        SelectStandardCourse();
                    }
                });
            }
            var radios = document.getElementsByName('choose_sku'); // 获取所有name为exampleRadio的radio按钮
            for(var i = 0; i < radios.length; i++) {
                radios[i].addEventListener('change', function(event) { // 为每个按钮添加change事件监听
                var showComingNum= document.getElementById('appoint_skuid');
                    if (this.value === 'appoint') {
                       showComingNum.style.display = 'flex'; // 隐藏按钮
                    }else{
                       showComingNum.style.display = 'none'; // 显示按钮
                    }
                    if(this.checked) { // 确保只有被选中的按钮会触发
                        SelectStandardCourse();
                    }
                });
            }
            var radios = document.getElementsByName('choose_url'); // 获取所有name为exampleRadio的radio按钮
            for(var i = 0; i < radios.length; i++) {
                radios[i].addEventListener('change', function(event) { // 为每个按钮添加change事件监听
                    if(this.checked) { // 确保只有被选中的按钮会触发
                          SelectStandardCourse();
                    }
                });
            }

            const inputElement = document.getElementById('searchInput');
                let timeoutId;
                inputElement.addEventListener('input', function() {
                    // 清除之前的定时器
                    clearTimeout(timeoutId);
                    // 设置新的定时器
                    timeoutId = setTimeout(function() {
                        const inputValue = inputElement.value;
                        console.log('输入框内容:', inputValue);
                        SelectStandardCourse();
                    }, 1000); // 1秒后调用search函数
                });
    });




    function ImportOrder(sku_id,marketing_id,choose_env){
        document.getElementById("result").innerText = "生成中,请等待...";
        let mobile=document.getElementById("mobile").value;
            var modalOverlay = document.querySelector('.modal-overlay');
            if  (document.getElementById("result").innerText ="生成中,请等待..."){
                console.log("123123123123123")
                    modalOverlay.style.display = 'block';
            }
            var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
            var url = '/hualala_import_order/py/hualalaImportOrder'+
                "?choose_env="+choose_env+
                "&mobile="+mobile+
                "&sku_id="+sku_id+
                "&marketing_id="+marketing_id;
            httpRequest.open('GET', url, true);//第二步：打开连接
            httpRequest.send();//第三步：发送请求  将请求参数写在URL中
            httpRequest.onreadystatechange = function () {
                if (httpRequest.readyState === 4 && httpRequest.status === 200) {
                     var json = httpRequest.responseText;//获取到json字符串，还需解析
                    document.getElementById("result").innerText = json;
                    modalOverlay.style.display = 'none';
                    alert(json);
                    }
                }
        }

    function SelectStandardCourse(){
        var envbox=document.getElementById("choose_env");
        radios=envbox.getElementsByTagName("input");
        var inputElement1 = document.getElementById('course1');
        var inputElement2 = document.getElementById('course2');
        var inputElement3 = document.getElementById('course3');
        var inputElement4 = document.getElementById('course4');
        var inputElement5 = document.getElementById('course5');
        var inputElement6 = document.getElementById('course6');
        var inputElement7 = document.getElementById('course7');
        for(i=0;i<radios.length;i++){
            if(radios[i].checked) {
                choose_env = radios[i].value;
                console.log("选中的环境是: " +choose_env);
                if(choose_env == "test"){
                    inputElement1.value = '1955,1963,1826';
                    inputElement2.value = '313,314,1989';
                    inputElement3.value = '201,206,207,2118,2325,2328,2388';
                    inputElement4.value = '202,203,208,209';
                    inputElement5.value = '301,302,303,304';
                    inputElement6.value = '310,311,312,309';
                    inputElement7.value = '1957,1958,2394,2395';
                    console.log("whywhywhy")
                }else{
                    inputElement1.value = '1593';
                    inputElement2.value = '313,314';
                    inputElement3.value = '200,201,206,207,1623';
                    inputElement4.value = '202,203,208,209';
                    inputElement5.value = '301,302,303,304';
                    inputElement6.value = '310,311,312';
                    inputElement7.value = '1589';
                }
                break; // 找到后退出循环
            }
        }
        var choose_sku = document.getElementsByName("choose_sku");
        const inputElement = document.getElementById('searchInput');
        for(i = 0; i < choose_sku.length; i++) {
            if(choose_sku[i].checked) {
                var choose_sku_id = choose_sku[i].value;
                console.log("选中的套餐是: " + choose_sku_id);
                if (choose_sku_id == "appoint"){
                    choose_sku_id = inputElement.value;
                    console.log("输入的套餐是: " + choose_sku_id);
                }
                break; // 找到后退出循环
            }
        }
        var PaintingTools = document.getElementsByName("PaintingTools");
        for(i = 0; i < PaintingTools.length; i++) {
            if(PaintingTools[i].checked) {
                 var choose_tools = PaintingTools[i].value;
                console.log("选中的画具是: " + PaintingTools[i].value);
                break; // 找到后退出循环
            }
        }

        if(choose_tools != null){
            document.getElementById('loading').style.display = 'block';
            var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
            var url = '/hualala_import_order/py/hualalaSelectApplyStandardCourse'+
                "?choose_env="+choose_env+
                "&choose_sku_id="+choose_sku_id+
                "&choose_tools="+choose_tools;
            httpRequest.open('GET', url, true);//第二步：打开连接
            httpRequest.send();//第三步：发送请求  将请求参数写在URL中
            httpRequest.onreadystatechange = function () {
                if (httpRequest.readyState === 4 && httpRequest.status === 200) {

                    document.getElementById('loading').style.display = 'none';
                    json = httpRequest.responseText;//获取到json字符串，还需解析
                    var obj=JSON.parse(httpRequest.responseText)
                    var jsonData=obj.data
                    let tbody = document.getElementById("applystandardcourse");
                      while (tbody.rows.length > 0) {
                            tbody.deleteRow(0);
                          }
                    if(jsonData.length == 0){
                        let row1= `<tr><td><div class="el-table__empty-block" style="height: 100%; width: 1327px;"><span class="el-table__empty-text">暂无数据</span></div></td></tr>`
                        tbody.insertAdjacentHTML('beforeend', row1); // 使用insertAdjacentHTML提高性能
                    }
                    jsonData.forEach(({ mealName, areaName, couponId,hasTools,originalPrice,price,courseMarketingId,marketingName,skuId,actualPrice }) => { // ES6解构赋值
                        // 创建一行<tr>${}
                        if (couponId === 1){var couponId = "有";}else if (couponId === 0){couponId = "无";}
                        if (hasTools === 1){var hasTools = "是";}else if (hasTools === 0){hasTools = "否";}
                        let row= `<tr><td rowspan="1" colspan="1" class="el-table_1_column_5 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">${skuId}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_1 is-center "><div class="cell el-tooltip" style="word-wrap: break-word"><span data-v-492e78dd="" class="bold">${mealName}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_2 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">中国大陆</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_3 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">首报全款</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_4 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">全量</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_14 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">${couponId}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_15 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">${hasTools}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_16 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">￥ ${price}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_17 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">￥ ${originalPrice}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_18 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">￥ ${actualPrice}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_19 is-center "><div class="cell el-tooltip" style="width: 78px;"><span data-v-492e78dd="">${courseMarketingId}</span></div></td><td rowspan="1" colspan="1" class="el-table_1_column_20 is-center"><div class="cell el-tooltip" style="word-wrap: break-word"><span>${marketingName}</span></div></td><td rowspan="1" colspan="1" class="el-table_2_column_14 is-center"><div class="cell el-tooltip" style="width: 138px;"><button data-v-492e78dd="" type="button" class="el-button el-button--primary el-button--small" onClick="passRowData(this)">确认购买</button></div></td></tr>`
                        // 将新行插入到tbody中
                        tbody.insertAdjacentHTML('beforeend', row); // 使用insertAdjacentHTML提高性能
                        // 获取所有确认按钮
                    });
                    }
                    document.addEventListener('DOMContentLoaded', function() {
                    // 获取页面中所有的button元素
                    var buttons = document.querySelectorAll('button');
                    // 遍历所有按钮
                    buttons.forEach(function(button) {
                        // 设置按钮为不可点击（置灰操作的一部分）
                        button.disabled = true;
                        // 可选：进一步通过CSS样式明确视觉上的禁用状态
                        // 通常情况下，设置disabled后浏览器会自动应用一些样式模拟置灰
                        // 但这里显式设置，确保跨浏览器一致性
                        button.style.opacity = '0.5'; // 降低透明度以呈现灰色
                        button.style.cursor = 'not-allowed'; // 更改鼠标悬停时的指针形状
                    });
                });
                }
                }

        }

    function passRowData(buttonElement) {
        // 找到按钮所在的行（tr）
        var row = buttonElement.closest('tr');
        var choose_sku_id = row.querySelectorAll('td')[0].textContent.trim();
        var marketing_id = row.querySelectorAll('td')[10].textContent.trim();
        ImportOrder(choose_sku_id,marketing_id,choose_env);
    }
    function test(sku_id,marketing_id,choose_env){
        console.log("分割线")
        console.log(sku_id,marketing_id,choose_env)
    }
    function validateInput(event) {
            const input = event.target;
            const value = input.value;
            // 使用正则表达式检查输入是否为正整数
            if (!/^[1-9]\d*$/.test(value)) {
                // 如果输入不是大于0的正整数，则清除非法字符
                input.value = value.replace(/[^1-9]/g, '');
            }
            if (value === '0' || value=="") {
                input.value = '1';
            }
            // 允许输入的最长数字长度
            const maxLength = 4;
            // 获取当前输入的值，去掉前导的+或-
            let currentValue = value.replace(/[^\d]/g, '');
            // 如果当前值的长度超过了最大长度，就裁剪它
            if (currentValue.length > maxLength) {
                currentValue = currentValue.substring(0, maxLength);
                input.value = currentValue;
            }
        }