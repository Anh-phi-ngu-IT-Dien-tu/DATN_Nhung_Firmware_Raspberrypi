#include "esp_camera.h"
#include <WiFi.h>

// ===================
// 🔹 Chọn Model Camera
// ===================
#define CAMERA_MODEL_AI_THINKER // Has PSRAM
#include "camera_pins.h"

// ===========================
// 🔹 Nhập WiFi Credentials
// ===========================
const char *ssid = "LAPTOP-Phi";
const char *password = "Phi18112003Laptop";

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // ===========================
  // 🔹 Cấu hình Camera
  // ===========================
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;  // Stream video dưới dạng JPEG
  config.frame_size = FRAMESIZE_UXGA;   // Đặt mặc định UXGA (1600x1200)
  config.jpeg_quality = 10;             // Chất lượng cao (0-63, thấp hơn = nét hơn)
  config.fb_count = 2;                   // Buffer đôi để tránh lag
  config.fb_location = CAMERA_FB_IN_PSRAM;

  if (!psramFound()) {
    Serial.println("❌ PSRAM không khả dụng! Giảm độ phân giải về VGA.");
    config.frame_size = FRAMESIZE_VGA;  // Nếu không có PSRAM, giảm xuống VGA
    config.fb_count = 1;
  }

  // ===========================
  // 🔹 Khởi động camera
  // ===========================
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("❌ Camera init failed! Lỗi 0x%x", err);
    return;
  }

  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    // s->set_vflip(s, 1);
    // s->set_hmirror(s, 1);
    s->set_quality(s, 10);       // Tăng chất lượng ảnh
    s->set_framesize(s, FRAMESIZE_UXGA);  // Đảm bảo UXGA
    s->set_brightness(s, 0);   // up the brightness just a bit
    s->set_saturation(s, 2);  // lower the saturation
    s->set_contrast(s, -2);
    // s->set_awb(s, 1);
    s->set_awb_gain(s, 1);
    s->set_wb_mode(s, 1);
    s->set_exposure_ctrl(s, 0);
    s->set_aec_value(s, 1000);
    s->set_aec2(s, 1);
    s->set_ae_level(s, 2);
    s->set_gain_ctrl(s, 0);
    s->set_agc_gain(s, 2);
    // s->set_agc_gain_ceiling(s, 3);
    s->set_bpc(s, 0);
    s->set_wpc(s, 1);
    s->set_raw_gma(s, 1);
    s->set_lenc(s, 1);
    s->set_dcw(s, 1);






  }

  // ===========================
  // 🔹 Kết nối WiFi
  // ===========================
  WiFi.begin(ssid, password);
  Serial.print("🔄 Đang kết nối WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi đã kết nối!");
  Serial.print("📷 Camera sẵn sàng tại: http://");
  Serial.println(WiFi.localIP());

  startCameraServer();
}

void loop() {
  delay(10000);
}
