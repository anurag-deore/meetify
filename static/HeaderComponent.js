"use strict";
const Header = () => {
    const [dmenuOpen, setdmenuOpen] = React.useState(false);
    return /*#__PURE__*/React.createElement("nav", {
      className: "navbar navbar-expand-lg shadow-sm navbar-light"
    }, /*#__PURE__*/React.createElement("div", {
      className: "container-fluid",
      id: "navContainer"
    }, /*#__PURE__*/React.createElement("a", {
      className: "logo theme-color",
      href: "/dashboard"
    }, "Meetify"), /*#__PURE__*/React.createElement("div", {
      className: "float-right d-flex justify-content-center align-items-center"
    }, /*#__PURE__*/window.location.href.indexOf("schedule") > -1 ? null : React.createElement("a", {
      className: "newbtn mr-4",
      href: "/schedule"
    }, "Schedule New Meet") , /*#__PURE__*/React.createElement("button", {
      onClick: () => setdmenuOpen(!dmenuOpen),
      className: "rounded-0 btn btn-default account-box"
    }, /*#__PURE__*/React.createElement("span", {
      className: "mdi acc mdi-account-outline"
    }, " "), /*#__PURE__*/dmenuOpen ? /*#__PURE__*/React.createElement("span", {
      className: "mdi acc mdi-chevron-up"
    }) : /*#__PURE__*/React.createElement("span", {
      className: "mdi acc mdi-chevron-down"
    })),/*#__PURE__*/React.createElement("div", {
      className: `dmenu shadow ${dmenuOpen ? "show" : ""}`,
      id: "dmenu"
    }, /*#__PURE__*/React.createElement("a", {
      className: "dropdown-item",
      href: "/dashboard"
    }, "DashBoard"), /*#__PURE__*/React.createElement("a", {
      className: "dropdown-item",
      href: "/mymeets"
    }, "Meets"),/*#__PURE__*/React.createElement("a", {
      className: "dropdown-item",
      href: "/profile"
    }, "Profile"), /*#__PURE__*/React.createElement("a", {
      className: "dropdown-item",
      href: "/logout"
    }, "Logout")))));
  };
  