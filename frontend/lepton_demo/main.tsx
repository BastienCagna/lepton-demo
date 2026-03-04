
import { startLeptonApp } from '@lepton/core/bootstrap'


function MyApp() {
    return (
        <div className='app'>
            <h1>Lepton Demo</h1>
        </div>
    )
}


startLeptonApp(<MyApp />);
