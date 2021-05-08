"use strict";
const Header = () => {
  const [dmenuOpen, setdmenuOpen] = React.useState(false);
  return React.createElement(
    "nav",
    {
      className: "navbar navbar-expand-lg shadow-sm navbar-light",
    },
    React.createElement(
      "div",
      {
        className: "container-fluid",
        id: "navContainer",
      },
      React.createElement(
        "a",
        {
          className: "logo theme-color",
          href: "/dashboard",
        },
        "Lec2Notes"
      ),
      React.createElement(
        "div",
        {
          className:
            "float-right d-flex justify-content-center align-items-center",
        },
        window.location.toString().indexOf("dashboard") != -1
          ? React.createElement(
              "a",
              {
                className: "newbtn mr-4",
                href: "/add",
              },
              "Add New Lecture"
            )
          : null,
        React.createElement(
          "button",
          {
            onClick: () => setdmenuOpen(!dmenuOpen),
            className: "rounded-0 btn btn-default account-box",
          },
          React.createElement(
            "span",
            {
              className: "mdi acc mdi-account-outline",
            },
            " "
          ),
          dmenuOpen
            ? React.createElement("span", {
                className: "mdi acc mdi-chevron-up",
              })
            : React.createElement("span", {
                className: "mdi acc mdi-chevron-down",
              })
        ),
        React.createElement(
          "div",
          {
            className: `dmenu shadow ${dmenuOpen ? "show" : ""}`,
            id: "dmenu",
          },
          React.createElement(
            "a",
            {
              className: "dropdown-item",
              href: "/dashboard",
            },
            "DashBoard"
          ),
          // React.createElement(
          //   "a",
          //   {
          //     className: "dropdown-item",
          //     href: "/mymeets",
          //   },
          //   "Meets"
          // ),
          React.createElement(
            "a",
            {
              className: "dropdown-item",
              href: "/profile",
            },
            "Profile"
          ),
          React.createElement(
            "a",
            {
              className: "dropdown-item",
              href: "/logout",
            },
            "Logout"
          )
        )
      )
    )
  );
};
