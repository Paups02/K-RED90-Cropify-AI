import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const CHART_COLORS = [
  'rgba(59, 130, 246, 0.8)',   // Blue
  'rgba(16, 185, 129, 0.8)',   // Green
  'rgba(249, 115, 22, 0.8)',   // Orange
  'rgba(139, 92, 246, 0.8)',   // Purple
  'rgba(236, 72, 153, 0.8)',   // Pink
  'rgba(245, 158, 11, 0.8)',   // Yellow
  'rgba(99, 102, 241, 0.8)',   // Indigo
  'rgba(20, 184, 166, 0.8)',   // Teal
];

const CHART_BORDERS = [
  'rgba(59, 130, 246, 1)',
  'rgba(16, 185, 129, 1)',
  'rgba(249, 115, 22, 1)',
  'rgba(139, 92, 246, 1)',
  'rgba(236, 72, 153, 1)',
  'rgba(245, 158, 11, 1)',
  'rgba(99, 102, 241, 1)',
  'rgba(20, 184, 166, 1)',
];

export default function ChartDisplay({ chartData }) {
  if (!chartData) return null;

  const { chart_type, title, labels, datasets, table_data } = chartData;

  // Prepare data for Chart.js
  const prepareChartData = () => {
    if (chart_type === 'pie' || chart_type === 'doughnut') {
      return {
        labels: labels || [],
        datasets: [{
          data: datasets?.[0]?.data || [],
          backgroundColor: CHART_COLORS,
          borderColor: CHART_BORDERS,
          borderWidth: 2,
        }],
      };
    }

    return {
      labels: labels || [],
      datasets: (datasets || []).map((ds, index) => ({
        label: ds.label || `Serie ${index + 1}`,
        data: ds.data || [],
        backgroundColor: CHART_COLORS[index % CHART_COLORS.length],
        borderColor: CHART_BORDERS[index % CHART_BORDERS.length],
        borderWidth: 2,
        tension: 0.3,
      })),
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: !!title,
        text: title || '',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: chart_type === 'pie' || chart_type === 'doughnut' ? {} : {
      y: {
        beginAtZero: true,
      },
    },
  };

  // Render table
  if (chart_type === 'table' && table_data) {
    const columns = table_data.length > 0 ? Object.keys(table_data[0]) : [];

    return (
      <div className="overflow-x-auto">
        {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table_data.map((row, rowIndex) => (
              <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                {columns.map((col) => (
                  <td key={col} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {row[col]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  // Render chart
  const data = prepareChartData();

  return (
    <div className="w-full h-80">
      {chart_type === 'bar' && <Bar data={data} options={chartOptions} />}
      {chart_type === 'line' && <Line data={data} options={chartOptions} />}
      {chart_type === 'pie' && <Pie data={data} options={chartOptions} />}
      {chart_type === 'doughnut' && <Doughnut data={data} options={chartOptions} />}
    </div>
  );
}
