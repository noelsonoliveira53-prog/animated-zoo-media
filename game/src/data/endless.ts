// Endless mode tuning: which enemies join as the waves climb, how fast health ramps and when bosses appear.

export interface EndlessTier {
  fromWave: number; // 1-based wave where these enemies join the pool
  enemies: string[];
}

export const ENDLESS = {
  waves: 200, // generated up front; nobody is expected to see the end
  hpRampPerWave: 0.07, // each wave's enemies get +7% health (compounding linearly on the level's hpMult)
  budgetBase: 260, // raw enemy HP per wave at wave 1 ...
  budgetPerWave: 70, // ... plus this much per wave
  maxGroupCount: 26,
  bossEvery: 10,
  nativeFrom: 5, // from this wave on, the map's own campaign enemies join the pool (its "home turf")
  bosses: ['murkmaw', 'grimtusk', 'vulkhar', 'morrowcap', 'saltjaw', 'kaleidrax', 'zephyrax', 'ulmaroth', 'grindmaw', 'velumbra', 'mawbloom', 'thrumhorn', 'scourmaw', 'brinecrown', 'dreadmast', 'rustantler', 'veilwhisker', 'crownmane', 'combqueen', 'glowmaw'],
  tiers: [
    { fromWave: 1, enemies: ['mudling', 'skitter', 'gloomwing', 'gnat'] },
    { fromWave: 4, enemies: ['shellback', 'bogmender', 'reedguard', 'wispling'] },
    { fromWave: 8, enemies: ['thornhog', 'splotch', 'puffcap', 'veilstalker'] },
    { fromWave: 12, enemies: ['bogbrute', 'rimewraith', 'cindermole', 'emberimp'] },
    { fromWave: 16, enemies: ['rootrager', 'ashhive'] },
    { fromWave: 20, enemies: ['barnaclad', 'gullwing', 'reefwarden'] },
    { fromWave: 24, enemies: ['shardskipper', 'mirrorback', 'glarefly'] },
    { fromWave: 28, enemies: ['galehound', 'cloudram', 'kitewing'] },
    { fromWave: 32, enemies: ['shiftscale', 'idolkeeper', 'bramblehide'] },
    { fromWave: 36, enemies: ['cogjammer', 'steamrunner', 'rivetshell'] },
    { fromWave: 40, enemies: ['dimlantern', 'echowisp', 'sparkeel'] },
    { fromWave: 44, enemies: ['barkwarden', 'seedcaster'] },
    { fromWave: 46, enemies: ['gorgegrub'] },
    { fromWave: 48, enemies: ['stormcaller', 'thunderhoof'] },
    { fromWave: 50, enemies: ['copperhorn'] },
    { fromWave: 52, enemies: ['shimmerjack', 'sandpicker'] },
    { fromWave: 54, enemies: ['kilnback'] },
    { fromWave: 56, enemies: ['shellsnap', 'tidecaller'] },
    { fromWave: 58, enemies: ['inkspitter'] },
    { fromWave: 60, enemies: ['deckgunner', 'ironkeel'] },
    { fromWave: 62, enemies: ['powdermonkey'] },
    { fromWave: 64, enemies: ['barkdrum', 'turnleaf'] },
    { fromWave: 66, enemies: ['sapstoat'] },
    { fromWave: 68, enemies: ['mistfox', 'silkcrane'] },
    { fromWave: 70, enemies: ['glowbearer'] },
    { fromWave: 72, enemies: ['howler', 'mourner'] },
    { fromWave: 74, enemies: ['harrier'] },
    { fromWave: 76, enemies: ['waxback', 'hexguard'] },
    { fromWave: 78, enemies: ['honeypaw'] },
    { fromWave: 80, enemies: ['lanternfrog', 'hexcroak'] },
    { fromWave: 82, enemies: ['mudskipper'] },
    { fromWave: 84, enemies: ['tumblehog', 'bloomdoe'] },
    { fromWave: 86, enemies: ['marmot'] },
  ] as EndlessTier[],
  attackRamp: 0.15, // enemy melee hits grow 8% per wave so blockers can't stall forever
  heroRegen: 0.5, // long runs reward tanky regen heroes too much; halve hero healing in endless
  // Daily mutator: one of these daily modifiers applies to every endless run that day.
  mutators: ['swift', 'tough', 'thrifty', 'rich', 'nospells', 'frenzy'],
  hardMutatorReward: 1.5, // payout multiplier when today's mutator makes runs harder
  rewardPerWave: { coins: 12, glowsap: 12 }, // village payout per wave held
};
