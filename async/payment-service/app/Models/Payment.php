<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Payment extends Model
{
    protected $fillable = [
        'order_id',
        'user_id',
        'amount',
        'payment_method',
        'payment_status',
        'payment_date'
    ];

    protected $dispatchesEvents = [
        'created' => \App\Events\PaymentCreated::class,
        'updated' => \App\Events\PaymentCreated::class,
    ];
}
