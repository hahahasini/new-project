import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function ConfidenceChart({ scores }) {
  const labels = scores.map((s) => s.label);
  const values = scores.map((s) => s.confidence);

  const data = {
    labels,
    datasets: [
      {
        label: 'Confidence (%)',
        data: values,
        backgroundColor: [
          'rgba(99, 102, 241, 0.6)',
          'rgba(6, 182, 212, 0.6)',
          'rgba(139, 92, 246, 0.6)',
          'rgba(245, 158, 11, 0.6)',
          'rgba(16, 185, 129, 0.6)',
          'rgba(239, 68, 68, 0.6)',
        ],
        borderColor: [
          'rgba(99, 102, 241, 1)',
          'rgba(6, 182, 212, 1)',
          'rgba(139, 92, 246, 1)',
          'rgba(245, 158, 11, 1)',
          'rgba(16, 185, 129, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 1,
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 1.8,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#f1f5f9',
        bodyColor: '#94a3b8',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        callbacks: {
          label: (ctx) => `${ctx.parsed.y.toFixed(1)}%`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#94a3b8',
          font: { size: 11, family: 'Inter' },
          maxRotation: 45,
        },
        grid: { display: false },
        border: { display: false },
      },
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          color: '#64748b',
          font: { size: 11, family: 'Inter' },
          callback: (v) => `${v}%`,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.04)',
        },
        border: { display: false },
      },
    },
  };

  return <Bar data={data} options={options} />;
}

export default ConfidenceChart;
