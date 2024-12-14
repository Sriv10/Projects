import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import {
  Autocomplete,
  LoadingOverlay,
  MantineProvider,
  Stack,
  Table,
} from "@mantine/core";
import axios from "axios";

function App() {
  const [data, setData] = useState([]);
  const [plays, setPlays] = useState([]);
  const [accuracy, setAccuracy] = useState(0);
  const [ndcg, setNdcg] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/games").then((response) => {
      var data = response.data.games.map((val: string) => {
        var description = val.split(",");
        return { value: description[1], label: description[0] };
      });
      setData(data);
    });
  }, []);

  const rows = plays.map((play: any) => (
    <Table.Tr key={play.playId}>
      <Table.Td>{play.description}</Table.Td>
      <Table.Td>{play.predictedWpa}</Table.Td>
    </Table.Tr>
  ));

  return (
    <MantineProvider>
      <Stack>
        <LoadingOverlay visible={loading} />
        <Autocomplete
          label="Select game"
          data={data}
          onOptionSubmit={(value) => {
            setLoading(true);
            axios
              .get(`http://127.0.0.1:8000/game?gameId=${value}`)
              .then((response) => {
                setLoading(false);
                setAccuracy(response.data.accuracy);
                setPlays(response.data.predictions);
                setNdcg(response.data.ndcg);
                console.log(response);
              });
          }}
        />
        <p>Accuracy {accuracy}%</p>
        <p>NDCG {ndcg}%</p>

        <Table>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Play Description</Table.Th>
              <Table.Th>Predicted WPA</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Stack>
    </MantineProvider>
  );
}

export default App;
