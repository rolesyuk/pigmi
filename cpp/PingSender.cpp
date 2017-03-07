//
// PingSender.cpp
// ~~~~~~~~~~
//
#include "PingSender.hpp"

//PingSender(std::string my_ip, std::Vector<std::string> remote_ips)
PingSender::PingSender(std::string new_my_ip, std::string new_remote_ip)
{
    my_ip = new_my_ip;
    remote_ip = new_remote_ip;
}

std::string PingSender::make_timestamp()
{
    struct timeval now;
    long double now_in_seconds;
    gettimeofday(&now, NULL);
    now_in_seconds = now.tv_sec + now.tv_usec / 1000000.0;
    return std::to_string(now_in_seconds);
}

std::string PingSender::pad_ip(std::string ip)
{
    std::string padding = " ";
    for (int i=0; i < 15 - ip.length(); i++)
    {
        padding = padding + " ";
    }
    return padding + ip;
}

void PingSender::send_ping()
{
    try
    {
        std::string outgoing_msg;
        boost::asio::io_service io_service;
        udp::resolver resolver(io_service);
        udp::resolver::query query(udp::v4(), remote_ip, port_num);
        udp::endpoint receiver_endpoint = *resolver.resolve(query);

        udp::socket socket(io_service);
        socket.open(udp::v4());
        outgoing_msg = make_timestamp() + pad_ip(my_ip); 
        socket.send_to(boost::asio::buffer(outgoing_msg), receiver_endpoint);
    }
    catch (std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }
}
