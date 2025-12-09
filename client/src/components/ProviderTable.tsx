import { DataGrid, type GridRowsProp, type GridColDef } from "@mui/x-data-grid";
import type { ProviderSearch } from "../types/provider";

interface ProviderTableProps {
  providerSearch: ProviderSearch;
}
export default function ProviderTable({ providerSearch }: ProviderTableProps) {
  const rows: GridRowsProp = providerSearch.results.map((prov) => {
    const name = prov.first_name
      ? prov.last_name + ", " + prov.first_name
      : prov.last_name;

    const location = prov.street_2
      ? prov.street_1 + ", " + prov.street_2 + ", " + prov.zipcode
      : prov.street_1 + ", " + prov.zipcode;

    return {
      id: prov.id,
      name: name,
      credentials: prov.credentials ?? "--",
      location: location,
      accepts_medicare: prov.accepts_medicare,
      total_benes: prov.total_benes,
      avg_age: prov.avg_age,
    };
  });

  const columns: GridColDef[] = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "credentials", headerName: "Credentials", width: 100 },
    { field: "location", headerName: "Location", width: 400 },
    { field: "accepts_medicare", headerName: "Medicare", width: 80 },
    { field: "total_benes", headerName: "Total Patients", width: 125 },
    { field: "avg_age", headerName: "Avg. Patient Age", width: 150 },
  ];

  if (!providerSearch.success) {
    return <p>Search Failed: {providerSearch.error}</p>;
  }

  return (
    <div>
      <div>
        <p>
          Found <b>{providerSearch.count}</b>{" "}
          {providerSearch.results[0].specialty} provider
          {providerSearch.count > 1 ? "s" : ""} in{" "}
          <b>
            {providerSearch.results[0].city}, {providerSearch.results[0].state}
            {providerSearch.parsed_params.zipcode
              ? ", " + providerSearch.parsed_params.zipcode
              : ""}
          </b>
        </p>
      </div>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { pageSize: 25, page: 0 },
          },
        }}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    </div>
  );
}
