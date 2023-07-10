// Initialize the bracket viewer
var bracket = new BracketsViewer('#bracket', {
  // Set the tournament structure
  tournament: {
    type: 'ingle-elimination',
    nodes: [
      {
        name: 'Round 1',
        children: [
          {
            name: 'Match 1',
            teams: ['Team 1', 'Team 2']
          },
          {
            name: 'Match 2',
            teams: ['Team 3', 'Team 4']
          },
          {
            name: 'Match 3',
            teams: ['Team 5', 'Team 6']
          }
        ]
      },
      {
        name: 'Round 2',
        children: [
          {
            name: 'Match 1',
            teams: ['Team 1', 'Team 3']
          },
          {
            name: 'Match 2',
            teams: ['Team 2', 'Team 4']
          },
          {
            name: 'Match 3',
            teams: ['Team 5', 'Team 6']
          }
        ]
      },
      {
        name: 'Final',
        children: [
          {
            name: 'Match 1',
            teams: ['Team 1', 'Team 2']
          },
          {
            name: 'Match 2',
            teams: ['Team 3', 'Team 4']
          },
          {
            name: 'Match 3',
            teams: ['Team 5', 'Team 6']
          }
        ]
      }
    ]
  },

  // Set the team names and colors
  teams: [
    {
      name: 'Team 1',
      color: '#ff0000'
    },
    {
      name: 'Team 2',
      color: '#00ff00'
    },
    {
      name: 'Team 3',
      color: '#0000ff'
    },
    {
      name: 'Team 4',
      color: '#ffff00'
    },
    {
      name: 'Team 5',
      color: '#ff00ff'
    },
    {
      name: 'Team 6',
      color: '#00ffff'
    }
  ]
});
