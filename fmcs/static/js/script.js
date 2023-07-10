const { JsonDatabase } = require('brackets-json-db');
const { BracketsManager } = require('brackets-manager');

const storage = new JsonDatabase();
const manager = new BracketsManager(storage);

// Create an elimination stage for tournament `3`.
await manager.create.stage({
  tournamentId: 3,
  name: 'Elimination stage',
  type: 'double_elimination',
  seeding: ['Team 1', 'Team 2', 'Team 3', 'Team 4'],
  settings: { grandFinal: 'double' },
});

await manager.update.match({
  id: 0, // First match of winner bracket (round 1)
  opponent1: { score: 16, result: 'win' },
  opponent2: { score: 12 },
});