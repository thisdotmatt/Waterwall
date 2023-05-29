import './App.css';
function App() {
  return (
    <Home />
  );
}

export default App;

function Home() {
  return (
    <>
    <div className='nav-bar'>
      <div className='nav-bar-logo'>
        <img src="" alt="Waterwall Logo"/>
      </div>
      <div className='nav-bar-links'>
        <ul>
          <li>HOME</li>
          <li>PRODUCTS</li>
          <li>CONTACT</li>
          <li>LOGIN</li>
        </ul>
      </div>
    </div>
    <div className='main-content'>
      <div className='main-content-col1'>
        <div className='heading-1'>
          <h1 className='heading-text'>Protecting your technology</h1>
          <h1 className='heading-text'>with the click of a button.</h1>
        </div>
        <div className='heading-2'>
          <p className='paragraph-text'>We provide only the best, most affordable products
          on the market. Our customizable firewall is state-of-the-art and has won nearly
          a dozen cybersecurity awards.</p>
        </div>
        <div className='cta-div'>
          <div className='cta-main'>
            <button>Try It Out</button>
          </div>
          <div className='cta-secondary'>
            <button>Learn More</button>
          </div>
        </div>
      </div>

      <div className='main-content-col2'>
        <div className='earth-image'>
          <img src="" alt="Earth Image"/>
        </div>
        <div className='image-sub-div'>
          <p className='image-sub-text'>
            Serving Communities Worldwide<b/>
            It's Who We Are.
          </p>
        </div>
      </div>
    </div>
    </>
  );
}