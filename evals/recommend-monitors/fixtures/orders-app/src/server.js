const express = require('express');
const Stripe = require('stripe');
const { supabase } = require('./lib/supabase');
require('./jobs/nightly-export');

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

app.use(express.static('public')); // serves /login (login form page)
app.use('/webhooks/stripe', express.raw({ type: 'application/json' }));
app.use(express.json());

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) return res.status(401).json({ error: 'invalid credentials' });
  res.json({ token: data.session.access_token });
});

app.get('/api/orders', async (req, res) => {
  const { data } = await supabase.from('orders').select('*').order('created_at', { ascending: false });
  res.json(data);
});

app.post('/api/orders', async (req, res) => {
  const intent = await stripe.paymentIntents.create({
    amount: req.body.amount,
    currency: 'eur',
  });
  const { data } = await supabase.from('orders').insert({ amount: req.body.amount, payment_intent: intent.id, status: 'pending' }).select();
  res.status(201).json(data[0]);
});

app.get('/api/reports/weekly', async (req, res) => {
  const { data } = await supabase.rpc('weekly_report');
  res.json(data);
});

app.post('/webhooks/stripe', (req, res) => {
  const event = stripe.webhooks.constructEvent(req.body, req.headers['stripe-signature'], process.env.STRIPE_WEBHOOK_SECRET);
  if (event.type === 'payment_intent.succeeded') {
    supabase.from('orders').update({ status: 'paid' }).eq('payment_intent', event.data.object.id).then(() => {});
  }
  res.json({ received: true });
});

app.listen(process.env.PORT || 3000);
