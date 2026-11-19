const cron = require('node-cron');
const { supabase } = require('../lib/supabase');

// Every night at 02:00: export the day's paid orders for the accountant.
cron.schedule('0 2 * * *', async () => {
  const { data } = await supabase.from('orders').select('*').eq('status', 'paid');
  await supabase.storage.from('exports').upload(`orders-${Date.now()}.json`, JSON.stringify(data));
});
