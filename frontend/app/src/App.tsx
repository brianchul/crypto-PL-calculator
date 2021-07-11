
import MainPage from "./components/mainPage";
import { PageHeader } from "antd";

import 'antd/dist/antd.css';
import './App.css'

function App() {
  return (
    <>
      <PageHeader
        className="site-page-header"
        title="Crypto Dex tools"
        subTitle=""
        backIcon={false}
      />
      <MainPage/>
      <PageHeader
        className="site-page-header"
        title=""
        subTitle=""
        backIcon={false}
      />
    </>

  );
}

export default App;
