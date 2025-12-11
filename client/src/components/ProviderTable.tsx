import { DataGrid, type GridRowsProp, type GridColDef } from "@mui/x-data-grid";
import LinearProgress from "@mui/material/LinearProgress";
import styles from "./ProviderTable.module.css";

import type {
  ProviderScoreResponse,
  ProviderSearchResponse,
  ScoredProvider,
} from "../types/provider";

function ScoreCell({ score }: { score: number }) {
  const getColor = (score: number) => {
    if (score >= 80) return "#4caf50";
    if (score >= 60) return "#ffeb3b";
    if (score >= 40) return "#ff9800";
    return "#f44336";
  };

  return (
    <div className={styles.score}>
      <p>{score}</p>
      <div style={{ flex: 1, marginLeft: "0.5rem" }}>
        <LinearProgress
          variant="determinate"
          value={score}
          sx={{
            height: 8,
            borderRadius: 4,
            backgroundColor: "#e0e0e0",
            "& .MuiLinearProgress-bar": {
              backgroundColor: getColor(score),
              borderRadius: 4,
            },
          }}
        />
      </div>
    </div>
  );
}

interface ProviderTableProps {
  tableData: ProviderSearchResponse | ProviderScoreResponse | null;
  isLoading: boolean;
}
export default function ProviderTable({
  tableData,
  isLoading,
}: ProviderTableProps) {
  function isScoreResponse(
    data: ProviderSearchResponse | ProviderScoreResponse
  ): data is ProviderScoreResponse {
    return data.results.length > 0 && "score" in data.results[0];
  }

  const skeletonRows: GridRowsProp = Array.from({ length: 10 }).map((_, i) => ({
    id: `skeleton-${i}`,
  }));

  const columns: GridColDef[] = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "credentials", headerName: "Credentials", width: 100 },
    { field: "location", headerName: "Location", width: 400 },
    { field: "accepts_medicare", headerName: "Medicare", width: 80 },
    { field: "total_benes", headerName: "Total Patients", width: 125 },
    { field: "avg_age", headerName: "Avg. Patient Age", width: 150 },
  ];

  if (!tableData) {
    return (
      <DataGrid
        loading={isLoading}
        rows={skeletonRows}
        columns={columns}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    );
  }

  if (isScoreResponse(tableData)) {
    columns.unshift(
      { field: "rank", headerName: "Rank", width: 100 },
      {
        field: "score",
        headerName: "Score",
        width: 150,
        renderCell: (params) => <ScoreCell score={params.value} />,
      }
    );
  }

  const rows: GridRowsProp = tableData.results.map((prov) => {
    const baseRow = {
      id: prov.id,
      name: prov.first_name
        ? `${prov.last_name}, ${prov.first_name}`
        : prov.last_name,
      credentials: prov.credentials ?? "--",
      location: prov.street_2
        ? `${prov.street_1}, ${prov.street_2}, ${prov.zipcode}`
        : `${prov.street_1}, ${prov.zipcode}`,
      accepts_medicare: prov.accepts_medicare,
      total_benes: prov.total_benes,
      avg_age: prov.avg_age,
    };

    if (isScoreResponse(tableData)) {
      const scoredProv = prov as ScoredProvider;
      return {
        ...baseRow,
        score: Number(scoredProv.score.toFixed(2)),
        rank: scoredProv.rank,
      };
    }

    return baseRow;
  });

  if (!tableData.success) {
    return <p>Search Failed: {tableData.error}</p>;
  }

  return (
    <div>
      <DataGrid
        loading={isLoading}
        rows={rows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { pageSize: 10, page: 0 },
          },
        }}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    </div>
  );
}
