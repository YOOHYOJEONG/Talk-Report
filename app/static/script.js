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


// 사용자별 메시지 수 그래프
function drawUserCountChart(userCount) {
    const users = Object.keys(userCount);
    const counts = Object.values(userCount);

    const trace = {
        x: users,
        y: counts,
        type: "bar",
        marker: { color: "#4A90E2" },
    };

    const layout = {
        title: "사용자별 메시지 수",
        xaxis: { title: "사용자" },
        yaxis: { title: "메시지 수" },
    };

    Plotly.newPlot("userChart", [trace], layout);
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
        title: "시간대별 메시지 수",
        xaxis: { title: "시간 (0~23시)" },
        yaxis: { title: "메시지 수" },
    };

    Plotly.newPlot("hourChart", [trace], layout);
}