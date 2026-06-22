<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Faker\Factory as Faker;

class PaymentSeeder extends Seeder
{
    public function run(): void
    {
        $methods = ['credit_card', 'bank_transfer', 'ewallet', 'cash'];
        $statuses = ['pending', 'success', 'failed'];

        for ($i = 0; $i < 50; $i++) {
            DB::table('payments')->insert([
                'order_id' => rand(1, 50),
                'user_id' => rand(1, 50),
                'amount' => rand(15, 200) * 1000,
                'payment_method' => $methods[array_rand($methods)],
                'payment_status' => $statuses[array_rand($statuses)],
                'payment_date' => now()->subDays(rand(1, 30)),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
