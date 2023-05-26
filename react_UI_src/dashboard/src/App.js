import './App.css';
function App() {
  return (
    <Home {...homeData} />
  );
}

export default App;

function Home(props) {
  const {
    waterwall_logo,
    protectingYourTech,
    weProvideOnlyThe,
    globe,
    servingCommunities,
    comp12,
    comp11,
    comp122,
    comp13,
    comp5,
    comp7,
  } = props;

  return (
    <div className = "container-center-horizontal">
      <div className= "home screen">
        <div className = "flex-col">
          <div className = "flex-row">
            <img className="waterwall_logo" src={waterwall_logo} alt="Waterwall Logo" />
            <Component12 place={comp12.place}/>
            <Component1>{comp11.children}</Component1>
            <Component1 className={comp122.className}>
              {comp122.children}
            </Component1>
            <Component1 className={comp13.className}>
              {comp13.children}
            </Component1>
          </div>
          <h1 className="protecting-your-tech outfit-normal-white-55px">{protectingYourTech}</h1>
        </div>
        <div className="flex-row-1">
          <div className="flew-col-1">
            <p className="we-provide-only-the outfit-light-white-25px">
              {weProvideOnlyThe}
            </p>
          </div>
        </div>
      </div>
    </div>

  )
}