import { Link } from 'react-router-dom';

import styles from './MainNavigation.module.css';

const MainNavigation = () => {

    return (
        <header className={styles.header}>
            <div className={styles.logo}>Evolutionary Computing</div>
            <nav>
                <ul>
                    <li>
                        <Link to='/'>Home</Link>
                    </li>
                    <li>
                        <Link to='/classic-EA'>Classical EA</Link>
                    </li>
                </ul>
            </nav>
        </header>
    )
}

export default MainNavigation;