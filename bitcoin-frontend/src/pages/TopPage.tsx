import { Card, Grid, Text, Container, Title } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import classes from "../css/Card.module.css";

const TopPage = () => {
  const navigate = useNavigate();

  const handleCardClick = (path: string) => {
    navigate(path); // React Routerを使ってURLに遷移
  };

  const cardInfo = {
    wallet: { title: "MyWallet", comment: "自分の財布", path: "wallet" },
    chain: { title: "BlockChain", comment: "Chainの中身の確認", path: "chain" },
    soon1: { title: "Mining", comment: "Let's Mining", path: "mining" },
    soon2: { title: "取引所", comment: "取引しよう", path: "trade" },
  };

  return (
    <Grid>
      {Object.values(cardInfo).map((card, index) => (
        <Grid.Col span={6} key={index}>
          <Card
            className={classes.mainCard}
            onClick={() => handleCardClick(`/${card.path}`)}
          >
            <Title>{card.title}</Title>
            <Text>{card.comment}</Text>
          </Card>
        </Grid.Col>
      ))}
    </Grid>
  );
};

export default TopPage;
