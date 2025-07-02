// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/gsoc2025-Sakhineti_Praveena/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/";
          },
        },{id: "post-week-4-jun-23-jun-29",
        
          title: "Week 4 (Jun 23 - Jun 29)",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Week-4/";
          
        },
      },{id: "post-week-3-jun-16-jun-22",
        
          title: "Week 3 (Jun 16 - Jun 22)",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Week-3/";
          
        },
      },{id: "post-week-2-jun-09-jun-15",
        
          title: "Week 2 (Jun 09 - Jun 15)",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Week-2/";
          
        },
      },{id: "post-week-1-jun-01-jun-08",
        
          title: "Week 1 (Jun 01 - Jun 08)",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Week-1/";
          
        },
      },{id: "post-community-bonding-week-2",
        
          title: "Community Bonding Week-2",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Community-Bonding-Week-2/";
          
        },
      },{id: "post-community-bonding-week-1",
        
          title: "Community Bonding Week-1",
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/gsoc2025-Sakhineti_Praveena/blog/2025/Community-Bonding-Week-1/";
          
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
