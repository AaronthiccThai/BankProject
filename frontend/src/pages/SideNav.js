import React from "react";

const SideNav = ({ isOpen, toggleNav}) => {
    return (
        <div>
            <div className={`sidenav ${isOpen ? "sidenav-open" : "sidenav-closed"}`}>
                <button onClick={toggleNav} className="closeButton">
                    &times;
                </button>
                <a href="#">About</a>
                <a href="#">Contacts</a>
            </div>
        </div>
    );
};

export default SideNav;
