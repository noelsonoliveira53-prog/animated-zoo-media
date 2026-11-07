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
  bosses: ['murkmaw', 'grimtusk', 'vulkhar', 'morrowcap', 'saltjaw', 'kaleidrax'],
  tiers: [
    { fromWave: 1, enemies: ['mudling', 'skitter', 'gloomwing', 'gnat'] },
    { fromWave: 4, enemies: ['shellback', 'bogmender', 'reedguard', 'wispling'] },
    { fromWave: 8, enemies: ['thornhog', 'splotch', 'puffcap', 'veilstalker'] },
    { fromWave: 12, enemies: ['bogbrute', 'rimewraith', 'cindermole', 'emberimp'] },
    { fromWave: 16, enemies: ['rootrager', 'ashhive'] },
    { fromWave: 20, enemies: ['barnaclad', 'gullwing', 'reefwarden'] },
    { fromWave: 24, enemies: ['shardskipper', 'mirrorback', 'glarefly'] },
  ] as EndlessTier[],
  attackRamp: 0.15, // enemy melee hits grow 8% per wave so blockers can't stall forever
  heroRegen: 0.5, // long runs reward tanky regen heroes too much; halve hero healing in endless
  rewardPerWave: { coins: 12, glowsap: 12 }, // village payout per wave held
};
