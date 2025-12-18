document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    const file = document.getElementById("file").files[0];
    const start = document.getElementById("start_date").value;
    const end = document.getElementById("end_date").value;

    formData.append("file", file);
    formData.append("start_date", start);
    formData.append("end_date", end);

    const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();

    document.getElementById("totalMessages").innerText =
        `총 메시지 수: ${data.total}`;

    drawUserCountChart(data.user_count);
    drawHourlyChart(data.hour_count);
});


function drawUserCountChart(userCount) {
    // 1) 메시지 수 기준 내림차순 정렬
    const sorted = Object.entries(userCount)
        .sort((a, b) => b[1] - a[1]);

    const users = sorted.map(item => item[0]);
    const counts = sorted.map(item => item[1]);

    // 2) 그래프 그리기
    const trace = {
        x: users,
        y: counts,
        type: "bar",
        marker: { color: "#4A90E2" },
    };

    const layout = {
        xaxis: {
            tickangle: -45,
            automargin: true
        },
        yaxis: { title: "메시지 수" },
        margin: { b: 150 }
    };

    Plotly.newPlot("userChart", [trace], layout);

    // 3) 테이블도 같이 생성
    drawUserTable(sorted);
}

function drawUserTable(sorted) {
    const table = document.getElementById("userTable");

    // 테이블 초기화
    table.innerHTML = `
        <tr style="background:#f2f2f2; font-weight:bold;">
            <th>순위</th>
            <th>사용자</th>
            <th>메시지 수</th>
        </tr>
    `;

    sorted.forEach((item, idx) => {
        const user = item[0];
        const count = item[1];

        const row = `
            <tr>
                <td>${idx + 1}</td>
                <td>${user}</td>
                <td>${count}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

// 시간대별 메시지 수 그래프
function drawHourlyChart(hourCount) {
    const hours = Object.keys(hourCount).map(Number);
    const counts = Object.values(hourCount);

    const trace = {
        x: hours,
        y: counts,
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#FF7043" },
    };

    const layout = {
        xaxis: { title: "시간 (0~23시)" },
        yaxis: { title: "메시지 수" },
    };

    Plotly.newPlot("hourChart", [trace], layout);
}