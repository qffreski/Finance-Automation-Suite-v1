# Finance Automation Suite v1

Aplikasi automation untuk upload voucher ke sistem Kingdee dengan GUI yang user-friendly.

## ✨ Fitur Utama

- **GUI Desktop** - Interface modern menggunakan PySide6
- **Excel Reader** - Baca data voucher dari file Excel (.xlsx, .xls)
- **Auto Calibration** - Tentukan koordinat UI target dengan mudah
- **Smart Automation** - Otomatis klik dan input data sesuai koordinat
- **PDF Upload** - Upload attachment PDF otomatis
- **Progress Tracking** - Monitor progress upload real-time
- **Auto Performance Detection** - Sistem otomatis detect performa hardware dan adjust kecepatan
- **Async UI** - UI tetap responsif saat proses berjalan

## 🚀 Mulai Cepat

### Requirements

- Python 3.10+
- Windows OS (untuk pyautogui compatibility)

### Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application:**
   ```bash
   python main.py
   ```

### Folder Structure

```
Finance-Automation-Suite-v1/
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Dependencies
├── OPTIMIZATION_GUIDE.md   # Panduan optimasi (BACA INI!)
│
├── config/
│   ├── config_manager.py        # Config management
│   ├── calibration.py           # Calibration tool (async)
│   └── performance_detector.py   # Auto performance detection
│
├── core/
│   ├── app_context.py      # Application context
│   └── logger.py           # Logging system
│
├── gui/
│   ├── main_window.py      # Main window
│   ├── upload_page.py      # Upload tab
│   └── setting_page.py     # Settings tab
│
├── modules/
│   ├── excel_reader.py           # Baca Excel
│   ├── file_selector.py          # File selection logic
│   ├── kingdee_automation.py     # Automation logic
│   └── upload_worker.py          # Upload worker thread
│
├── models/
│   └── voucher.py          # Voucher data model
│
├── logs/
│   └── app.log             # Application log file
```

## 📋 Cara Penggunaan

### Step 1: Calibration (Pertama Kali)

1. Buka aplikasi → Tab **Settings**
2. Di section **"Calibration"**, klik setiap tombol untuk posisi yang ingin dikalibrasi
3. Dalam 5 detik, **pindahkan mouse ke UI element target** di aplikasi Kingdee
4. Sistem akan otomatis menyimpan koordinat

**Daftar positions:**
- query, checkbox, option, attachment, new, plus, file_name, open, save, exit1, exit2, error

### Step 2: Prepare Excel File

Buat file Excel dengan kolom:
| VoucherNumber | VoucherPDF | UkuranPDF |
|---------------|-----------|----------|
| V001          | file1.pdf | 100      |
| V002          | file2.pdf | 150      |

**Requirements:**
- Kolom **VoucherNumber** wajib ada
- Kolom **VoucherPDF** wajib ada (path ke PDF file)
- Kolom **UkuranPDF** opsional (ukuran dalam KB)

### Step 3: Run Upload

1. Buka aplikasi → Tab **Upload**
2. Klik **"Pilih Excel"** dan pilih file Excel Anda
3. Pastikan aplikasi Kingdee sudah terbuka dan siap
4. Klik **"Start Upload"** untuk mulai automation
5. Monitor progress di log area

### Step 4: Monitor & Troubleshoot

- Lihat **log messages** untuk detail setiap voucher
- Jika ada error, baca pesan error di log
- Progress bar menunjukkan persentase selesai
- Klik **"Stop"** untuk stop process

## 🔧 Performance Optimization

### Auto Detection

Aplikasi **otomatis mendeteksi performa system** Anda:

- **SLOW Profile** - Komputer low-end (CPU ≤2, RAM ≤4GB)
- **NORMAL Profile** - Komputer standar
- **FAST Profile** - Komputer powerful (CPU ≥8, RAM ≥16GB)

Setiap profile memiliki timing yang sudah di-optimize. **Tidak perlu manual setup!**

### Cek Profile Anda

1. Buka Tab **Settings**
2. Lihat bagian **"Performance Profile"**
3. Sistem menampilkan:
   - Profile name (SLOW/NORMAL/FAST)
   - Timing multiplier
   - Adjusted delays

### Manual Tuning (Optional)

Jika ingin fine-tune timing secara manual:

1. Tab **Settings** → Section **"Timing Adjustment"**
2. Adjust parameter sesuai kebutuhan:
   - **Move Duration** - Kecepatan mouse bergerak
   - **Click Delay** - Jeda setelah klik
   - **Search Delay** - Jeda setelah search
   - **Dialog Delay** - Jeda saat dialog muncul
3. Klik **"Save Timing Settings"**

**Tips:**
- Kursor lambat? Increase **Move Duration**
- Aplikasi timeout? Increase **Click/Search/Dialog Delay**
- Upload terlalu cepat? Increase delays secara general

Lihat **OPTIMIZATION_GUIDE.md** untuk panduan lengkap!

## 🆕 Apa Yang Baru di v1

### Fix: "Not Responding" saat Capture Koordinat ✅

**Masalah Lama:**
- Saat capture countdown, UI freeze (not responding)
- User harus tunggu 5 detik sebelum bisa interact

**Solution (v1):**
- Capture sekarang menggunakan **QThread worker** (async)
- UI tetap responsif saat countdown
- Koordinat muncul smooth tanpa freeze

### Feature: Auto Performance Detection ✅

**Masalah Lama:**
- Kursor lambat di komputer lain
- User harus manual adjust timing
- Tidak tahu setting apa yang tepat

**Solution (v1):**
- Sistem auto-detect CPU, RAM, usage
- Timing di-adjust otomatis per profile
- Profile info ditampilkan di Settings tab
- Manual override tetap available jika perlu

### Improvement: Better Logging ✅

- Log file: `logs/app.log`
- System info di-log pada startup
- Performance profile di-log
- Detailed error messages

## ⚙️ Configuration

Semua setting disimpan di:
```
C:\Users\[YourUsername]\AppData\Roaming\Finance Automation Suite\config.json
```

**Jangan edit manual kecuali tahu apa yang dilakukan!**

Gunakan GUI Settings tab untuk adjust configuration.

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 | Windows 10/11 |
| Python | 3.10 | 3.10+ |
| CPU | 2 cores | 4+ cores |
| RAM | 4GB | 8GB+ |
| Resolution | 1280x720 | 1920x1080+ |

## 🐛 Troubleshooting

### Kursor Lambat

1. Cek tab **Settings** → Performance Profile
2. Jika SLOW, sistem sudah auto-adjust. Tunggu lebih lama
3. Jika masih lambat, manual increase timing di **Timing Adjustment**

### "Not Responding" saat Capture

✅ **Sudah di-fix di v1!** Capture sekarang async, UI tetap responsif.

### Koordinat Tidak Akurat

1. Pastikan aplikasi target posisi sama saat kalibrasi
2. Jika monitor resolution berubah, kalibrasi ulang
3. Gunakan **"Reset All Calibration"** untuk reset semua

### Upload Gagal / Error

1. Baca error message di log tab
2. Check bahwa PDF file path benar
3. Ensure aplikasi target (Kingdee) dalam keadaan valid
4. Try test dengan 1 voucher dulu

Lihat **OPTIMIZATION_GUIDE.md** untuk troubleshooting lengkap.

## 📁 Log Files

Log disimpan di:
```
./logs/app.log
```

Gunakan log file untuk:
- Debug error
- Track history automation
- Monitor performance

## 📝 License

Private Project

## 👨‍💻 Developer

Created with ❤️

---

**⭐ Pro Tips:**

1. **Baca OPTIMIZATION_GUIDE.md** - Panduan lengkap optimization & troubleshooting
2. **Calibrate terlebih dahulu** - Jangan skip calibration
3. **Test dengan batch kecil** - Coba 2-3 vouchers dulu sebelum batch besar
4. **Monitor log** - Selalu perhatian ke log messages
5. **Backup config** - Backup `config.json` sebelum update aplikasi

---

**Last Updated:** July 2024
**Version:** 1.0 (Auto-Optimization Release)
