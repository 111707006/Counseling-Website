// 日曆排程系統 JavaScript 功能

// 初始化日曆
function initializeCalendar() {
    console.log('初始化日曆，事件數量:', allEvents.length);
    const calendarEl = document.getElementById('calendar');
    
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'zh-tw',
        height: 'auto',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
            today: '今天',
            month: '月檢視',
            week: '週檢視',
            day: '日檢視'
        },
        events: allEvents,
        eventClick: function(info) {
            showAppointmentDetails(info.event);
        },
        eventMouseEnter: function(info) {
            // 滑鼠懸停效果
            info.el.style.transform = 'scale(1.05)';
            info.el.style.zIndex = '100';
        },
        eventMouseLeave: function(info) {
            // 滑鼠離開效果
            info.el.style.transform = 'scale(1)';
            info.el.style.zIndex = 'auto';
        },
        dayMaxEvents: 3,
        moreLinkClick: 'popover',
        moreLinkText: function(num) {
            return '還有 ' + num + ' 個預約';
        },
        eventDisplay: 'block',
        displayEventTime: true,
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        slotMinTime: '08:00:00',
        slotMaxTime: '20:00:00',
        allDaySlot: false,
        nowIndicator: true,
        weekends: true,
        // 自定義事件渲染
        eventDidMount: function(info) {
            // 添加工具提示
            const tooltip = createTooltip(info.event);
            info.el.setAttribute('title', tooltip);
            
            // 添加額外的樣式類
            const therapistId = info.event.extendedProps.therapistId;
            if (therapistId) {
                info.el.classList.add('therapist-' + therapistId);
            }
            
            // 如果沒有完整時間槽，添加特殊樣式
            if (!info.event.extendedProps.hasSlot) {
                info.el.style.border = '2px dashed #e74c3c';
                info.el.style.opacity = '0.7';
                info.el.title += '\n⚠️ 待安排確切時間';
            }
        }
    });
    
    calendar.render();
}

// 創建工具提示內容
function createTooltip(event) {
    const props = event.extendedProps;
    const startTime = new Date(event.start).toLocaleTimeString('zh-TW', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    let tooltip = `預約時間: ${startTime}
心理師: ${props.therapist}
諮商室: ${props.room}
電話: ${props.phone}
狀態: ${props.status}`;

    // 如果沒有完整時間槽，添加提醒
    if (!props.hasSlot) {
        tooltip += '\n⚠️ 待安排確切時間';
    }
    
    return tooltip;
}

// 顯示預約詳情彈窗
function showAppointmentDetails(event) {
    const modal = document.getElementById('appointmentModal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const editBtn = document.getElementById('edit-appointment-btn');
    
    const props = event.extendedProps;
    const startDate = new Date(event.start);
    const endDate = new Date(event.end);
    
    // 設置標題
    modalTitle.textContent = `預約詳情 #${props.appointmentId}`;
    
    // 設置編輯連結
    editBtn.href = `/admin/appointments/appointment/${props.appointmentId}/change/`;
    
    // 生成詳情內容
    modalBody.innerHTML = `
        <div class="detail-grid">
            <div class="detail-label">👤 個案姓名:</div>
            <div class="detail-value">${event.title}</div>
            
            <div class="detail-label">📧 電子郵件:</div>
            <div class="detail-value">${props.email}</div>
            
            <div class="detail-label">📱 聯絡電話:</div>
            <div class="detail-value">${props.phone || '未提供'}</div>
            
            <div class="detail-label">👨‍⚕️ 心理師:</div>
            <div class="detail-value">${props.therapist}</div>
            
            <div class="detail-label">📅 預約日期:</div>
            <div class="detail-value">${startDate.toLocaleDateString('zh-TW')}</div>
            
            <div class="detail-label">🕐 預約時間:</div>
            <div class="detail-value">${startDate.toLocaleTimeString('zh-TW', {hour: '2-digit', minute: '2-digit'})} - ${endDate.toLocaleTimeString('zh-TW', {hour: '2-digit', minute: '2-digit'})}</div>
            
            <div class="detail-label">🏢 諮商室:</div>
            <div class="detail-value">${props.room}</div>
            
            <div class="detail-label">💻 諮商方式:</div>
            <div class="detail-value">${props.consultationType}</div>
            
            <div class="detail-label">📋 狀態:</div>
            <div class="detail-value">
                <span style="background-color: #c6f6d5; color: #22543d; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                    ${props.status}
                </span>
                ${!props.hasSlot ? '<br><span style="color: #e74c3c; font-size: 12px;">⚠️ 待安排確切時間</span>' : ''}
            </div>
            
            ${props.notes ? `
                <div class="detail-label">📝 管理員備註:</div>
                <div class="detail-value" style="grid-column: 1 / -1; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                    ${props.notes}
                </div>
            ` : ''}
        </div>
    `;
    
    // 顯示彈窗
    modal.style.display = 'block';
}

// 關閉彈窗
function closeModal() {
    document.getElementById('appointmentModal').style.display = 'none';
}

// 點擊彈窗外部關閉
window.onclick = function(event) {
    const modal = document.getElementById('appointmentModal');
    if (event.target === modal) {
        closeModal();
    }
}

// 更新統計數據
function updateStatistics() {
    console.log('更新統計數據，事件數量:', allEvents.length);
    
    const today = new Date();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - today.getDay());
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);
    
    let todayCount = 0;
    let weekCount = 0;
    let therapistSet = new Set();
    
    allEvents.forEach(event => {
        const eventDate = new Date(event.start);
        
        // 今日預約
        if (eventDate.toDateString() === today.toDateString()) {
            todayCount++;
        }
        
        // 本週預約
        if (eventDate >= startOfWeek && eventDate <= endOfWeek) {
            weekCount++;
        }
        
        // 活躍心理師
        if (event.extendedProps.therapistId) {
            therapistSet.add(event.extendedProps.therapistId);
        }
    });
    
    console.log('統計結果:', {
        total: allEvents.length,
        today: todayCount,
        week: weekCount,
        therapists: therapistSet.size
    });
    
    document.getElementById('total-appointments').textContent = allEvents.length;
    document.getElementById('today-appointments').textContent = todayCount;
    document.getElementById('week-appointments').textContent = weekCount;
    document.getElementById('active-therapists').textContent = therapistSet.size;
}

// 生成心理師色彩圖例
function generateLegend() {
    const legendContainer = document.getElementById('legend-container');
    const therapists = {};
    
    // 收集所有心理師信息
    allEvents.forEach(event => {
        const therapistId = event.extendedProps.therapistId;
        const therapistName = event.extendedProps.therapist;
        
        if (therapistId && therapistName && !therapists[therapistId]) {
            therapists[therapistId] = therapistName;
        }
    });
    
    // 生成圖例項目
    let legendHTML = '';
    for (const [therapistId, therapistName] of Object.entries(therapists)) {
        const color = therapistColors[therapistId] || therapistColors.default;
        legendHTML += `
            <div class="legend-item">
                <div class="legend-color" style="background-color: ${color};"></div>
                <span>${therapistName}</span>
            </div>
        `;
    }
    
    if (legendHTML === '') {
        legendHTML = '<div class="legend-item">暫無預約數據</div>';
    }
    
    legendContainer.innerHTML = legendHTML;
}

// 匯出到 Excel
function exportToExcel() {
    // 準備匯出數據
    const exportData = allEvents.map(event => {
        const startDate = new Date(event.start);
        const props = event.extendedProps;
        
        return {
            '預約編號': props.appointmentId,
            '個案姓名': event.title,
            '電子郵件': props.email,
            '聯絡電話': props.phone || '',
            '心理師': props.therapist,
            '日期': startDate.toLocaleDateString('zh-TW'),
            '時間': startDate.toLocaleTimeString('zh-TW', {hour: '2-digit', minute: '2-digit'}),
            '諮商室': props.room,
            '諮商方式': props.consultationType,
            '狀態': props.status,
            '備註': props.notes || ''
        };
    });
    
    // 使用簡單的 CSV 匯出（可以被 Excel 開啟）
    const csvContent = convertToCSV(exportData);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `預約排程_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 轉換為 CSV 格式
function convertToCSV(objArray) {
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = '';
    
    // 添加 BOM 以支持中文
    str = '\uFEFF';
    
    // 標題行
    const headers = Object.keys(array[0]);
    str += headers.join(',') + '\r\n';
    
    // 數據行
    for (let i = 0; i < array.length; i++) {
        let line = '';
        for (let index in array[i]) {
            if (line !== '') line += ',';
            line += '"' + (array[i][index] || '').toString().replace(/"/g, '""') + '"';
        }
        str += line + '\r\n';
    }
    
    return str;
}

// 匯出到 PDF
function exportToPDF() {
    // 創建打印友好的頁面
    const printWindow = window.open('', '_blank');
    const currentDate = new Date().toLocaleDateString('zh-TW');
    
    let tableHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>預約排程報表</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: 'Microsoft JhengHei', sans-serif; margin: 20px; }
                h1 { text-align: center; color: #333; }
                .info { text-align: center; margin-bottom: 30px; color: #666; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 12px; }
                th { background-color: #f8f9fa; font-weight: bold; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .therapist-name { font-weight: bold; color: #667eea; }
                .status { padding: 2px 6px; border-radius: 4px; font-size: 11px; }
                .status-confirmed { background-color: #c6f6d5; color: #22543d; }
                @media print {
                    body { margin: 0; }
                    .no-print { display: none; }
                }
            </style>
        </head>
        <body>
            <h1>心理諮商預約排程表</h1>
            <div class="info">
                <p>報表產生日期：${currentDate}</p>
                <p>總預約數：${allEvents.length}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>編號</th>
                        <th>個案姓名</th>
                        <th>心理師</th>
                        <th>日期</th>
                        <th>時間</th>
                        <th>諮商室</th>
                        <th>諮商方式</th>
                        <th>聯絡電話</th>
                        <th>狀態</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    // 按日期排序
    const sortedEvents = [...allEvents].sort((a, b) => new Date(a.start) - new Date(b.start));
    
    sortedEvents.forEach(event => {
        const startDate = new Date(event.start);
        const props = event.extendedProps;
        
        tableHTML += `
            <tr>
                <td>${props.appointmentId}</td>
                <td>${event.title}</td>
                <td class="therapist-name">${props.therapist}</td>
                <td>${startDate.toLocaleDateString('zh-TW')}</td>
                <td>${startDate.toLocaleTimeString('zh-TW', {hour: '2-digit', minute: '2-digit'})}</td>
                <td>${props.room}</td>
                <td>${props.consultationType}</td>
                <td>${props.phone || ''}</td>
                <td><span class="status status-confirmed">${props.status}</span></td>
            </tr>
        `;
    });
    
    tableHTML += `
                </tbody>
            </table>
            <div class="no-print" style="margin-top: 30px; text-align: center;">
                <button onclick="window.print()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">列印 / 儲存為 PDF</button>
                <button onclick="window.close()" style="background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-left: 10px;">關閉</button>
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(tableHTML);
    printWindow.document.close();
}

// 鍵盤快捷鍵
document.addEventListener('keydown', function(event) {
    // ESC 關閉彈窗
    if (event.key === 'Escape') {
        closeModal();
    }
    
    // Ctrl+E 匯出 Excel
    if (event.ctrlKey && event.key === 'e') {
        event.preventDefault();
        exportToExcel();
    }
    
    // Ctrl+P 匯出 PDF
    if (event.ctrlKey && event.key === 'p') {
        event.preventDefault();
        exportToPDF();
    }
});

// 響應式調整
window.addEventListener('resize', function() {
    if (calendar) {
        calendar.updateSize();
    }
});

// 搜尋功能
function searchAppointments(query) {
    if (!query) {
        calendar.removeAllEvents();
        calendar.addEventSource(allEvents);
        return;
    }
    
    const filteredEvents = allEvents.filter(event => {
        const searchText = query.toLowerCase();
        return (
            event.title.toLowerCase().includes(searchText) ||
            event.extendedProps.therapist.toLowerCase().includes(searchText) ||
            event.extendedProps.email.toLowerCase().includes(searchText) ||
            event.extendedProps.phone.includes(searchText)
        );
    });
    
    calendar.removeAllEvents();
    calendar.addEventSource(filteredEvents);
    updateStatistics();
}

// 添加搜尋框（如果需要的話）
function addSearchBox() {
    const filterSection = document.querySelector('.filter-section form .filter-row');
    if (filterSection) {
        const searchGroup = document.createElement('div');
        searchGroup.className = 'filter-group';
        searchGroup.innerHTML = `
            <label for="search">搜尋</label>
            <input type="text" id="search" placeholder="姓名、心理師、電話..." 
                   onkeyup="searchAppointments(this.value)">
        `;
        filterSection.appendChild(searchGroup);
    }
}