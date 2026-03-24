function selectFiles() {
    document.getElementById("fileInput").click();
}

function selectFolder() {
    document.getElementById("folderInput").click();
}

function formatNumber(value) {
    const number = Number(value);

    if (Number.isNaN(number)) {
        return value;
    }

    return String(Math.trunc(number)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// 선택된 파일 개수 표시
function updateSelectedInfo() {
    const files = [
        ...document.getElementById("fileInput").files,
        ...document.getElementById("folderInput").files
    ];
    document.getElementById("selectedInfo").innerText =
        files.length ? `선택된 파일: ${formatNumber(files.length)}개` : "";
}

document.getElementById("fileInput").addEventListener("change", updateSelectedInfo);
document.getElementById("folderInput").addEventListener("change", updateSelectedInfo);

document.getElementById("analyzeBtn").addEventListener("click", async () => {
    const formData = new FormData();
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;

    const files = [
        ...document.getElementById("fileInput").files,
        ...document.getElementById("folderInput").files
    ];

    if (!files.length) {
        alert("파일 또는 폴더를 선택해 주세요.");
        return;
    }

    if (!startDate || !endDate) {
        alert("시작일과 종료일을 모두 입력해 주세요.");
        return;
    }

    if (startDate > endDate) {
        alert("시작일은 종료일보다 늦을 수 없습니다.");
        return;
    }

    files.forEach(f => formData.append("files", f));

    formData.append("start_date", startDate);
    formData.append("end_date", endDate);

    const res = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (!res.ok) {
        alert(data.error || "분석 중 오류가 발생했습니다.");
        return;
    }

    document.getElementById("totalMessages").innerText =
        `총 메시지 수: ${formatNumber(data.total)}개`;

    drawUserChart(data.user_count);
    drawHourlyChart(data.hour_count);
});


function drawUserChart(userCount) {
    const sorted = Object.entries(userCount).sort((a, b) => b[1] - a[1]);
    Plotly.newPlot("userChart", [{
        x: sorted.map(v => v[0]),
        y: sorted.map(v => v[1]),
        type: "bar",
        text: sorted.map(v => formatNumber(v[1])),
        textposition: "auto",
        hovertemplate: "%{x}<br>메시지 수: %{text}개<extra></extra>"
    }], {
        yaxis: {
            tickformat: ",d"
        }
    });

    drawUserTable(sorted);
}

function drawUserTable(sorted) {
    const table = document.getElementById("userTable");
    table.innerHTML = `
        <tr>
            <th>순위</th>
            <th>사용자</th>
            <th>메시지 수</th>
        </tr>
    `;

    sorted.forEach(([user, count], i) => {
        table.innerHTML += `
            <tr>
                <td>${i + 1}</td>
                <td>${user}</td>
                <td>${formatNumber(count)}</td>
            </tr>
        `;
    });
}

function drawHourlyChart(hourCount) {
    Plotly.newPlot("hourChart", [{
        x: Object.keys(hourCount),
        y: Object.values(hourCount),
        type: "scatter",
        mode: "lines+markers",
        hovertemplate: "%{x}시<br>메시지 수: %{y:,d}개<extra></extra>"
    }], {
        yaxis: {
            tickformat: ",d"
        }
    });
}
