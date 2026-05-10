model api_post_module

species api_poster skills: [network] {
    string api_host <- "127.0.0.1";
    int api_port <- 8000;
    string api_endpoint <- "/from-gama";
    map api_headers <- ["Content-Type"::"application/json"];
    bool log_response <- true;

    init {
        do connect(to: api_host, protocol: "http", port: api_port, raw: true);
    }

    action post(map payload) {
        do send(
            to: api_endpoint,
            contents: [
                "POST",
                to_json(payload),
                api_headers
            ]
        );
    }

    reflex receive_reply {
        loop while: has_more_message() {
            message mess <- fetch_message();

            if log_response {
                write "API CODE:";
                write sample(map(mess.contents)["CODE"]);

                write "API BODY:";
                write sample(map(mess.contents)["BODY"]);
            }
        }
    }
}

//model MyModel
//
//// 匯入 API POST 模組
//// 如果你的主模型在 models/，模組在 includes/，就使用這個相對路徑
//import "../includes/api_post_module.gaml"
//
//global {
//    // 範例變數：你可以換成自己模型裡的變數
//    int total_vehicles <- 100;
//
//    init {
//        // 建立 1 個 API 發送代理
//        // 它只負責連線、POST payload、接收 response
//        create api_poster number: 1 {
//            // 本地 API 主機
//            api_host <- "127.0.0.1";
//
//            // 本地 API port
//            api_port <- 8000;
//
//            // API endpoint
//            // 最終會送到 http://127.0.0.1:8000/from-gama
//            api_endpoint <- "/from-gama";
//
//            // 是否在 GAMA console 印出 API 回覆
//            log_response <- true;
//        }
//    }
//
//    // 每 1 個 simulation cycle 發送一次 POST
//    // 如果不想太頻繁，可以改成 every(10 #cycles) 或 every(60 #cycles)
//    reflex send_payload_to_api when: every(1 #cycles) {
//        // 找到剛剛建立的 api_poster，請它發送 payload
//        ask one_of(api_poster) {
//            // 這裡就是你要送出去的 payload
//            // GAML 的 ["key"::value] 會被模組轉成 JSON
//            do post([
//                "model"::"MyModel",
//                "cycle"::cycle,
//                "vehicles"::total_vehicles
//            ]);
//        }
//    }
//}