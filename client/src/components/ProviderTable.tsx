import { DataGrid, type GridRowsProp, type GridColDef } from "@mui/x-data-grid";
import type { SearchResult } from "../types/search";

// function ScoreCell({ score }: { score: number }) {
//   const getColor = (score: number) => {
//     if (score >= 80) return "#4caf50";
//     if (score >= 60) return "#ffeb3b";
//     if (score >= 40) return "#ff9800";
//     return "#f44336";
//   };

//   return (
//     <div className={styles.score}>
//       <p>{score}</p>
//       <div style={{ flex: 1, marginLeft: "0.5rem" }}>
//         <LinearProgress
//           variant="determinate"
//           value={score}
//           sx={{
//             height: 8,
//             borderRadius: 4,
//             backgroundColor: "#e0e0e0",
//             "& .MuiLinearProgress-bar": {
//               backgroundColor: getColor(score),
//               borderRadius: 4,
//             },
//           }}
//         />
//       </div>
//     </div>
//   );
// }

interface ProviderTableProps {
  data: SearchResult | undefined;
  isLoading: boolean;
  paginationModel: {
    pageSize: number;
    page: number;
  };
  setPaginationModel: React.Dispatch<
    React.SetStateAction<{
      pageSize: number;
      page: number;
    }>
  >;
}
export default function ProviderTable({
  data,
  isLoading,
  paginationModel,
  setPaginationModel,
}: ProviderTableProps) {
  const columns: GridColDef[] = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "credentials", headerName: "Credentials", width: 100 },
    { field: "location", headerName: "Location", width: 400 },
    { field: "accepts_medicare", headerName: "Medicare", width: 80 },
    { field: "total_benes", headerName: "Total Patients", width: 125 },
    { field: "avg_age", headerName: "Avg. Patient Age", width: 150 },
  ];

  const rows: GridRowsProp =
    data?.result.map((prov) => ({
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
    })) ?? [];

  return (
    <div style={{ height: 500 }}>
      <DataGrid
        loading={isLoading}
        rows={rows}
        rowCount={data?.count ?? 0}
        columns={columns}
        paginationMode="server"
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    </div>
  );
}
