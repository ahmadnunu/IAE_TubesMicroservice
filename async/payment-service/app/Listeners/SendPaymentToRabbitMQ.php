<?php

namespace App\Listeners;

use App\Events\PaymentCreated;
use App\Services\RabbitMQService;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Facades\Log;

class SendPaymentToRabbitMQ
{
    protected $rabbitmqService;

    public function __construct(RabbitMQService $rabbitmqService)
    {
        $this->rabbitmqService = $rabbitmqService;
    }

    public function handle(PaymentCreated $event)
    {
        $payment = $event->payment;

        // Hanya kirim event ke RabbitMQ jika status pembayarannya adalah "paid" / "completed"
        if ($payment->payment_status === 'paid' || $payment->payment_status === 'completed') {
            $message = [
                'id' => $payment->id,
                'order_id' => $payment->order_id,
                'payment_status' => $payment->payment_status,
                'amount' => $payment->amount
            ];

            $messageJson = json_encode($message);

            try {
                // Publish dengan routing key 'payment.completed' sesuai yang didengarkan oleh Order Service
                $this->rabbitmqService->publish($messageJson, 'payment.completed');
                Log::info('Successfully published completed payment to RabbitMQ: ' . $messageJson);
            } catch (\Exception $e) {
                Log::error('Failed to publish completed payment to RabbitMQ: ' . $e->getMessage());
            }
        }
    }
}
