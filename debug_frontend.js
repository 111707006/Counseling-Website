// 在瀏覽器控制台中執行這段代碼來調試API連接
console.log('開始測試前端API連接...');

// 測試API連接
fetch('http://localhost:8000/api/therapists/profiles/')
  .then(response => {
    console.log('Response status:', response.status);
    console.log('Response headers:', [...response.headers.entries()]);
    return response.json();
  })
  .then(data => {
    console.log('✅ API連接成功！');
    console.log('心理師數量:', data.length);
    console.log('第一位心理師資料:', data[0]);
    
    // 檢查是否有consultation_modes欄位
    const firstTherapist = data[0];
    console.log('consultation_modes:', firstTherapist.consultation_modes);
    console.log('available_times:', firstTherapist.available_times);
    console.log('pricing:', firstTherapist.pricing);
  })
  .catch(error => {
    console.error('❌ API連接失敗:', error);
    console.error('錯誤詳情:', error.message);
  });

// 測試專業領域API
fetch('http://localhost:8000/api/therapists/specialties/')
  .then(response => response.json())
  .then(data => {
    console.log('✅ 專業領域API連接成功！');
    console.log('專業領域數量:', data.length);
    console.log('專業領域列表:', data.map(s => s.name));
  })
  .catch(error => {
    console.error('❌ 專業領域API連接失敗:', error);
  });