# Performance Optimization Guide

## 📊 Automatic Performance Detection

Finance Automation Suite **secara otomatis mendeteksi performa sistem** dan menyesuaikan kecepatan automation berdasarkan spesifikasi hardware.

### Bagaimana Cara Kerjanya?

Saat aplikasi startup, sistem akan:

1. **Detect CPU cores** - Jumlah processor cores yang tersedia
2. **Detect RAM** - Total memory dan penggunaan saat ini
3. **Menentukan Profile** - Slow, Normal, atau Fast
4. **Adjust Timing** - Otomatis mengatur delay untuk setiap operasi

Informasi lengkap dapat dilihat di tab **Settings**.

---

## 🎯 Performance Profiles

### SLOW Profile
**Kondisi:**
- CPU cores ≤ 2
- RAM ≤ 4GB
- RAM usage > 80%

**Karakteristik:**
- Timing multiplier: **1.5x** (50% lebih lambat)
- Mouse movement: **0.375s** (lebih smooth)
- Click delay: **1.2s** (lebih lama tunggu)
- Search delay: **4.5s** (lebih banyak waktu cari)

**Cocok untuk:** Laptop lama, VM (Virtual Machine), Komputer low-end

### NORMAL Profile
**Kondisi:**
- Sistem standar di antara SLOW dan FAST

**Karakteristik:**
- Timing multiplier: **1.0x** (standar)
- Mouse movement: **0.25s**
- Click delay: **0.8s**
- Search delay: **3.0s**

**Cocok untuk:** Komputer modern, laptop gaming, workstation

### FAST Profile
**Kondisi:**
- CPU cores ≥ 8
- RAM ≥ 16GB
- RAM usage < 50%

**Karakteristik:**
- Timing multiplier: **0.5x** (50% lebih cepat)
- Mouse movement: **0.125s** (sangat cepat)
- Click delay: **0.4s** (sangat responsif)
- Search delay: **1.5s** (cepat)

**Cocok untuk:** Server gaming, workstation powerful, komputer high-end

---

## ⚙️ Manual Timing Adjustment

Jika Anda ingin fine-tune timing secara manual:

1. Buka tab **Settings**
2. Scroll ke bawah ke section **"Timing Adjustment (Optional)"**
3. Adjust setiap parameter sesuai kebutuhan:
   - **Move Duration**: Kecepatan mouse bergerak (detik)
   - **Click Delay**: Jeda setelah klik (detik)
   - **Search Delay**: Jeda setelah search (detik)
   - **Dialog Delay**: Jeda saat dialog muncul (detik)
4. Klik **"Save Timing Settings"**

**Tips:**
- Jika mouse terlalu cepat/lambat, adjust **Move Duration**
- Jika aplikasi target "lag respond", increase **Click Delay**
- Jika search tidak ketemu, increase **Search Delay**

---

## 🎬 Calibration (Kalibrasi Koordinat)

Calibration adalah proses menentukan koordinat mouse untuk setiap UI element yang akan diklik.

### Cara Melakukan Calibration:

1. Buka tab **Settings**
2. Scroll ke section **"Calibration"**
3. Klik button untuk setiap posisi yang ingin dikalibrasi
4. **Dalam 5 detik, gerakkan mouse ke target element** (countdown akan menampilkan angka)
5. Tunggu hingga selesai - sistem akan menyimpan koordinat otomatis

### Daftar Positions yang Perlu Dikalibrasi:

| Position | Fungsi |
|----------|--------|
| query | Field pencarian voucher |
| checkbox | Checkbox data |
| option | Tombol opsi/menu |
| attachment | Tombol attachment |
| new | Tombol buat baru |
| plus | Tombol tambah |
| file_name | Field nama file |
| open | Tombol open/browse |
| save | Tombol simpan |
| exit1 | Tombol exit pertama |
| exit2 | Tombol exit kedua |
| error | Element error/notifikasi |

### ⚠️ Penting:
- Jangan pindahkan window/icon setelah kalibrasi
- Jika resolusi berubah, kalibrasi ulang
- Gunakan **"Reset All Calibration"** untuk reset semua

---

## 🔧 Troubleshooting

### Masalah: Kursor Lambat di Komputer Lain

**Solusi:**
- Cek tab Settings → lihat Performance Profile
- Jika "SLOW", sistem sudah auto-adjust. Tunggu prosesnya lebih lama
- Jika masih lambat, manual increase timing di section "Timing Adjustment"

**Contoh:**
```
Normal (1.0x):
  move_duration: 0.25s
  click_delay: 0.8s

Slow (1.5x):
  move_duration: 0.375s
  click_delay: 1.2s
```

### Masalah: "Not Responding" Saat Capture Koordinat

**Solusi:** ✅ SUDAH FIXED di versi ini!
- Capture sekarang menggunakan **async thread** (tidak freeze UI)
- UI tetap responsif saat countdown
- Koordinat muncul tanpa "not responding"

**Apa yang berubah:**
- Sebelum: `time.sleep()` blocking main thread → freeze
- Sekarang: `QThread` worker thread → smooth UI

### Masalah: Upload Terlalu Cepat/Lambat

**Penyebab utama:**
- `move_duration` terlalu pendek/panjang
- `click_delay` tidak sesuai
- `search_delay` tidak cukup untuk aplikasi target

**Solusi:**
1. Buka tab Settings
2. Manual adjust timing
3. Test dengan 1-2 voucher terlebih dahulu
4. Jika OK, lanjutkan batch

**Recommended Timing Increment:**
```
Terlalu cepat? Increase 0.3-0.5 detik per parameter
Terlalu lambat? Decrease 0.2-0.3 detik per parameter
```

### Masalah: Koordinat Tidak Akurat Setelah Kalibrasi

**Penyebab:**
- Monitor resolution berbeda
- Window position berubah
- Multi-monitor setup

**Solusi:**
1. Pastikan aplikasi target ada di **posisi yang sama** saat kalibrasi
2. Jangan ubah resolusi setelah kalibrasi
3. Jika berubah, lakukan **reset dan kalibrasi ulang**

---

## 📈 Performance Tips

### Untuk Sistem Slow (SLOW Profile):

```
✓ Close browser/aplikasi berat lainnya
✓ Disable antivirus realtime scanning (sementara)
✓ Increase all timing values by 20-30%
✓ Run automation saat tidak ada activity lain
```

### Untuk Sistem Normal (NORMAL Profile):

```
✓ Default timing sudah optimal
✓ Hanya adjust jika perlu spesifik
✓ Monitor CPU/RAM usage saat running
✓ Adjust search_delay jika aplikasi target lambat
```

### Untuk Sistem Fast (FAST Profile):

```
✓ Timing sudah di-optimize untuk kecepatan
✓ Monitor RAM usage (jangan sampai >80%)
✓ Bisa run multiple batch sequences
✓ Decrease timing jika aplikasi target timeout
```

---

## 🚀 Best Practices

1. **Always Calibrate First**
   - Jangan skip calibration
   - Calibrate di environment yang sama dengan production

2. **Test dengan Small Batch**
   - Jangan langsung run 100 vouchers
   - Test 2-3 vouchers dulu
   - Adjust timing jika diperlukan

3. **Monitor Log**
   - Buka tab "Upload"
   - Perhatikan log messages
   - Cek error messages untuk troubleshooting

4. **Regular Maintenance**
   - Restart aplikasi jika ada memory leak
   - Clear logs setiap bulan
   - Reset calibration jika monitor/resolusi berubah

5. **Backup Configuration**
   - Config disimpan di: `%APPDATA%\Finance Automation Suite\config.json`
   - Backup file ini sebelum update aplikasi

---

## 📝 Configuration File

Semua setting disimpan di:
```
C:\Users\[YourUsername]\AppData\Roaming\Finance Automation Suite\config.json
```

Struktur file:
```json
{
    "performance_profile": "normal",
    "timing_multiplier": 1.0,
    "move_duration": 0.25,
    "click_delay": 0.8,
    "search_delay": 3.0,
    "dialog_delay": 1.5,
    "attachment_delay": 2.0,
    "save_delay": 1.0,
    "countdown_delay": 1.0,
    "positions": {
        "query": [1156, 178],
        "checkbox": [334, 259],
        ...
    }
}
```

**Jangan edit manual kecuali tahu apa yang dilakukan!**

---

## ✅ Checklist Pre-Run

Sebelum menjalankan automation:

- [ ] Performance profile sudah dicek (Settings tab)
- [ ] Semua koordinat sudah dikalibrasi
- [ ] File Excel sudah di-prepare dengan benar
- [ ] Aplikasi target (Kingdee) sudah buka dan siap
- [ ] Timing adjustment sudah di-set (jika ada perubahan)
- [ ] Test run dengan 1-2 vouchers dulu
- [ ] Monitor running (jangan minimize window)

---

## 📞 Support

Jika ada masalah:

1. Check log file: `logs/app.log`
2. Screenshot error message
3. Note hardware specs: CPU cores, RAM, Resolution
4. Note timing settings yang dipakai
5. Describe langkah sebelum error terjadi

---

**Last Updated:** 2024
**Version:** 1.0 (Auto-Optimization)
